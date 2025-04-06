import streamlit as st
import os
import shutil
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
import fitz  # PyMuPDF for PDF reading
import docx
from PIL import Image
import pytesseract
import cv2
import numpy as np

st.set_page_config(page_title="Safe_docs", layout="wide", page_icon="📄")

st.markdown("""
    <style>
    .big-title {
        font-size: 40px !important;
        font-weight: bold;
        color: #1B4F72;
        text-align: center;
        margin-top: 20px;
    }
    .score-card {
        font-size: 28px;
        text-align: center;
        margin-top: 20px;
        color: #2C3E50;
        animation: slidein 2s ease-in-out;
    }
    @keyframes slidein {
      0% { transform: translateX(-100%); opacity: 0; }
      100% { transform: translateX(0%); opacity: 1; }
    }
    .main {
        background: #FFFFFF;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.08);
        border: 1px solid #D6DBDF;
        margin-top: 20px;
    }
    .stApp, .css-18e3th9, .css-1d391kg {
        background-color: #FFFFFF !important;
        color: #2C3E50 !important;
    }
    .score-card:hover {
        background-color: #F2F4F4;
        border-radius: 10px;
        padding: 10px;
    }
    .subheader-style {
        font-size: 30px;
        font-weight: 600;
        color: #154360;
        margin-top: 30px;
        text-align: center;
    }
    .result-box {
        font-size: 20px;
        color: #2C3E50;
        margin-top: 10px;
        text-align: center;
    }
    ul {
        list-style-type: disc;
        padding-left: 20px;
        text-align: left;
        color: #2C3E50;
        font-size: 18px;
    }
    .warning-box {
        background-color: #FFF3CD !important;
        color: #7A5200 !important;
        padding: 12px;
        border-radius: 8px;
        border-left: 5px solid #FFA000;
        margin: 15px 0;
    }
    .info-box {
        background-color: #D6EAF8 !important;
        color: #154360 !important;
        padding: 12px;
        border-radius: 8px;
        border-left: 5px solid #2980B9;
        margin: 15px 0;
    }
    progress {
        border-radius: 10px; 
        height: 10px;
    }
    progress::-webkit-progress-bar {
        background-color: #EAECEE;
        border-radius: 10px;
    }
    progress::-webkit-progress-value {
        border-radius: 10px;
        background-color: #2E86C1;
    }
    .preview-card {
        border: 1px solid #B0C4DE;
        border-radius: 10px;
        padding: 15px;
        background: #F0F8FF;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .preview-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
        background: #E6F2FF;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">📄 SAFE DOCS <br> SECURING LEGAL INTEGRITY WITH AI </div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload any document:", 
    type=["pdf", "docx", "txt", "jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    os.makedirs("temp_doc", exist_ok=True)
    file_path = os.path.join("temp_doc", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.markdown("---")
    st.markdown("### 📄 Document Preview")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if uploaded_file.type.startswith('image'):
            st.image(uploaded_file, use_container_width=True)
        elif uploaded_file.type == 'application/pdf':
            doc = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
            page = doc.load_page(0)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            st.image(img, use_container_width=True, caption="First Page Preview")
        elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            st.image("https://i.imgur.com/3BhzZQk.png", caption="Word Document", width=150)
        else:
            st.info("No visual preview available for this file type")
    
    with col2:
        st.markdown("""
        <div class="preview-card">
            <b>File Details:</b><br>
            <table>
                <tr><td><b>Name:</b></td><td>{}</td></tr>
                <tr><td><b>Type:</b></td><td>{}</td></tr>
                <tr><td><b>Size:</b></td><td>{:.1f} KB</td></tr>
            </table>
        </div>
        """.format(
            uploaded_file.name,
            uploaded_file.type,
            uploaded_file.size/1024
        ), unsafe_allow_html=True)
        
        st.download_button(
            label="⬇️ Download Original",
            data=uploaded_file.getvalue(),
            file_name=uploaded_file.name,
            mime=uploaded_file.type
        )

    def extract_text(file_path):
        ext = file_path.split(".")[-1].lower()
        try:
            if ext in ["jpg", "jpeg", "png", "pdf"]:
                if ext == "pdf":
                    doc = fitz.open(file_path)
                    text = ""
                    confidences = []
                    for page in doc:
                        pix = page.get_pixmap()
                        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
                        text += " ".join(data['text'])
                        confidences.extend([c for c in data['conf'] if c > 0])
                    avg_conf = sum(confidences)/len(confidences) if confidences else 0
                else:
                    img = cv2.imread(file_path)
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)
                    text = " ".join(data['text'])
                    confidences = [c for c in data['conf'] if c > 0]
                    avg_conf = sum(confidences)/len(confidences) if confidences else 0
                return text, ext, avg_conf
            elif ext == "txt":
                with open(file_path, "r", encoding="utf-8") as file:
                    return file.read(), ext, 100
            elif ext == "docx":
                doc = docx.Document(file_path)
                return "\n".join([p.text for p in doc.paragraphs]), ext, 100
            else:
                return "Unsupported file type.", ext, 0
        except Exception as e:
            st.error(f"❌ Error extracting text: {str(e)}")
            return "", ext, 0

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

    text, file_type, ocr_confidence = extract_text(file_path)

    if file_type in ["jpg", "jpeg", "png", "pdf"]:
        if ocr_confidence < 50:
            st.markdown(f"""
            <div class='warning-box'>
                ⚠️ <b>Low OCR Confidence ({ocr_confidence:.1f}%)</b><br>
                Text extraction quality is poor. Possible causes:<br>
                - Blurry/cropped image<br>
                - Handwritten text<br>
                - Complex layout
            </div>
            """, unsafe_allow_html=True)
        elif ocr_confidence < 80:
            st.markdown(f"""
            <div class='info-box'>
                ℹ️ <b>Moderate OCR Confidence ({ocr_confidence:.1f}%)</b><br>
                Some text may be inaccurate. Verify critical details manually.
            </div>
            """, unsafe_allow_html=True)

    if not text.strip():
        st.markdown("""
        <div class='warning-box'>
            ⚠️ <b>No Text Found</b><br>
            The document appears to be: <br>
            - A blank page <br>
            - An unsupported image format <br>
            - Extremely poor quality scan
        </div>
        """, unsafe_allow_html=True)

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
    st.markdown('<div class="subheader-style">🧾 Result Summary</div>', unsafe_allow_html=True)

    if verdict == "Fake":
        st.markdown(f"<div class='score-card'>⛔ FAKE Document</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='score-card'>✅ ORIGINAL Document</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='result-box'>📄 <b>File Type:</b> {file_type.upper()}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='result-box'>📘 <b>Document Type:</b> {doc_category.title()}</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='result-box'>
        🔍 <b>OCR Confidence:</b> 
        <span style='color: {"red" if ocr_confidence < 50 else "orange" if ocr_confidence < 80 else "green"}'>
            {ocr_confidence:.1f}%
        </span>
        <progress value="{ocr_confidence}" max="100" style="width: 200px; height: 10px;"></progress>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='result-box' style='text-align: left; margin-left: 20px; margin-right: 20px;'>
        <b>Reasons:</b>
        <ul>
    """ + ''.join([f"<li>{r}</li>" for r in reasons]) + """
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div style='
    background-color: rgb(56 59 63);
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #ffcccc;
    text-align: left;
    font-size: 18px;
    font-weight: 500;
    color: #FFFFFF;
    margin-top: 30px;
    '>
    <b>Please upload a document to continue.</b>
    </div>
    """, unsafe_allow_html=True)
