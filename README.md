Legal Document Analyzer - Smart AI & Forgery Detection

Overview
This project is an AI-powered tool designed to analyze legal documents, detect potential forgery, and summarize key clauses efficiently. It supports both PDFs and images, leveraging OCR, NLP, and image processing techniques.

Features
1. Upload Legal Document (PDF or Image)
Supports multi-page PDF and image uploads.

-->Uses OCR for text extraction:

-->Tesseract OCR for images.

-->PyMuPDF for PDFs.

2. AI-Powered Smart Text Analyzer
Summarizes long legal contracts.

Flags missing key clauses (e.g., “termination,” “non-compete,” “payment terms”).

Detects repeated or suspicious language.

Optional: Checks for inconsistent fonts and layout (basic forgery signs).

Technologies Used:

spaCy + keyword rules for legal term detection.

(Optional) GPT-2 / OpenAI API for in-depth summaries.

3. Smart Ink & Forgery Detection
Analyzes images for security ink patterns:

✅ UV ink presence.

✅ Fluorescent reaction.

✅ Color-shifting patterns (angle-based).

✅ Photochromic reaction (sunlight exposure).

Uses OpenCV to compare multiple versions of a document.

User Interaction: Prompts for specific image captures (e.g., "Please upload a photo of Page 3 under UV light").

4. Auto-Generated Legal Report
Provides a detailed report including:

✅ Detected security inks.

🧾 Summarized text.

⚠ Flags missing clauses or suspicious formatting.

Outputs a downloadable PDF report with findings.

Installation & Setup
Requirements
Python 3.x

Dependencies:

pip install pytesseract pymupdf spacy opencv-python numpy
Usage
Upload a legal document (PDF or image).

The system extracts text and runs an AI analysis.

If required, upload additional images under special lighting.

Generate and download the final report.

Future Enhancements
Real-time fraud detection alerts.

Integration with legal databases for validation.

More advanced AI models for clause detection.
