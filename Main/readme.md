📄 Document Authenticity Checker
Ever wondered if a document is real or fake? This simple web app lets you upload a document and checks its authenticity using some basic text analysis and keyword detection. Built with Streamlit, it supports PDFs, Word files, and plain text.

✨ What It Does
🔍 Reads documents and extracts text.

🧠 Checks for suspicious or scammy words.

🧾 Tries to figure out what kind of document it is — a certificate, ID, marksheet, or something legal.

✅ Tells you if the document seems original or fake, along with a few reasons why.

📚 What You Can Upload
This app can handle:

.pdf files
.docx Word documents
.txt plain text files

Other file types? Not yet supported.

🛠 How to Run It
Download the project
Clone the repo or just download the app.py file.

git clone https://github.com/your-username/document-authenticity-checker.git
cd document-authenticity-checker
Install the required Python packages
You can use a virtual environment if you like.

pip install -r requirements.txt
Run the app using Streamlit

streamlit run app.py
Use the app in your browser
Upload a file and see the results right there on the page.

🧠 How the Authenticity Check Works

The app uses a list of common "fake" words like:
winner, lottery, click, free, urgent, money, etc.
Each suspicious word adds points to a "fakeness score".
If the score is high (above 40), the app flags the document as fake.
It also shows you a few key reasons behind the verdict.

📘 Document Categories
Based on the words found in the file, the app tries to figure out if your document is:

🏆 A certificate
🆔 An ID proof
📈 A marksheet

⚖️ A legal document
Or just labels it as ❓ “Unknown” if it can’t tell.

🌱 What Could Be Added Next

OCR for scanned image-based PDFs
WordCloud to visualize common words
AI/NLP models for smarter detection
Let users give feedback on results

🤝 Want to Contribute?
Spotted something that could be better?
Fork the repo, make your changes, and create a pull request.
If it's a big idea, maybe open an issue first and let's talk.


📄 License
This project is open-source and uses the MIT License. So you're free to use, modify, and share it.

👋 About the Creator
Made by [Aman verma,Ayush Patial,Shivam Goyal,Harsh verma,Harshit bhatia]
