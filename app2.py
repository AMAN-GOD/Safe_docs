import streamlit as st
import os
import shutil
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
import fitz  # PyMuPDF for PDF reading
import docx

st.set_page_config(page_title="Document Authenticity Checker", layout="wide", page_icon="📄")

st.markdown("""
    <style>
    .big-title {
        font-size: 40px !important;
        font-weight: bold;
        color: #2E86C1;
        text-align: center;
        margin-top: 20px;
    }
    .score-card {
        font-size: 28px;
        text-align: center;
        margin-top: 20px;
        animation: slidein 2s ease-in-out;
    }
    @keyframes slidein {
      0% { transform: translateX(-100%); opacity: 0; }
      100% { transform: translateX(0%); opacity: 1; }
    }
    .cleaning-animation {
        font-size: 24px;
        text-align: center;
        margin-top: 20px;
        color: green;
        animation: trashAnim 1.5s ease-in-out;
    }
    @keyframes trashAnim {
      0% { transform: scale(1); opacity: 1; }
      50% { transform: scale(1.2); color: red; }
      100% { transform: scale(0); opacity: 0; }
    }
    .thankyou {
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        margin-top: 40px;
        color: #1ABC9C;
        animation: fadeinout 4s ease-in-out;
    }
    @keyframes fadeinout {
      0% { opacity: 0; }
      50% { opacity: 1; }
      100% { opacity: 0; }
    }
    .main {
        background: linear-gradient(to right, #f9f9f9, #e8f0fe);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    }
    body {
        background-color: #F4F6F7;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">📄 Document Authenticity Checker</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload any document:", type=None)

if uploaded_file is not None:
    os.makedirs("temp_doc", exist_ok=True)
    file_path = os.path.join("temp_doc", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    def extract_text(file_path):
        ext = file_path.split(".")[-1].lower()
        try:
            if ext == "txt":
                with open(file_path, "r", encoding="utf-8") as file:
                    return file.read(), ext
            elif ext == "pdf":
                doc = fitz.open(file_path)
                text = " ".join([page.get_text() for page in doc])
                return text, ext
            elif ext == "docx":
                doc = docx.Document(file_path)
                return "\n".join([p.text for p in doc.paragraphs]), ext
            else:
                return "Unsupported file type or empty file.", ext
        except Exception as e:
            st.error(f"❌ Error extracting text: {e}")
            return "", ext

    def classify_document_type(text):
        categories = {
            "certificate": ["certify", "certificate", "completion", "awarded"],
            "id": ["passport", "aadhaar", "identity", "id number", "dob"],
            "marksheet": ["marksheet", "grades", "score", "exam", "semester"],
            "legal": ["court", "law", "legal", "affidavit", "notary"]
        }
        text_lower = text.lower()
        for doc_type, keywords in categories.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return doc_type
        return "Unknown"

    text, file_type = extract_text(file_path)

    def assess_fakeness(text):
        if not text.strip():
            return 0.0, "Fake", ["Document is empty"]

        tfidf = TfidfVectorizer(stop_words='english')
        try:
            X = tfidf.fit_transform([text])
        except ValueError:
            return 0.0, "Fake", ["No valid words found"]

        fake_keywords = ["winner", "lottery", "prize", "click", "urgent", "guarantee", "money", "now", "free"]
        score = 0
        reasons = []

        for word in fake_keywords:
            if word in text.lower():
                score += 10
                reasons.append(f"Found suspicious word: {word}")

        final_score = min(score, 100)
        verdict = "Fake" if final_score > 40 else "Original"

        if verdict == "Fake" and len(reasons) < 3:
            reasons.extend(["Lacks official tone", "Contains promotional language", "Potential scam indicators"][:3 - len(reasons)])

        return final_score, verdict, reasons[:3]

    score, verdict, reasons = assess_fakeness(text)
    doc_category = classify_document_type(text)

    st.markdown('<div class="main">', unsafe_allow_html=True)

    st.subheader("🧾 Result Summary")
    if verdict == "Fake":
        st.markdown(f"<div class='score-card' style='color:red;'>⛔ FAKE Document</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='score-card' style='color:green;'>✅ ORIGINAL Document</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='score-card'>📄 File Type: {file_type.upper()}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='score-card'>📘 Document Type: {doc_category.title()}</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='score-card' style='font-size: 20px; color: #555;'>
    <ul>
    """ + ''.join([f"<li>{r}</li>" for r in reasons]) + """
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    
else:
    st.info("Please upload a document to continue.")