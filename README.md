# AI Notes Summarizer

An AI-powered PDF notes summarizer built using Python, Streamlit, Groq API, OCR, and PDF text extraction.

This tool can:

* Extract text from normal PDFs
* Automatically use OCR for scanned/image-based PDFs
* Generate:

  * Clean summaries
  * Important exam questions
  * Revision notes
  * Important keywords
* Display generated notes directly inside the app
* Allow users to download generated notes as a `.txt` file

---

# Features

* Hybrid PDF processing

  * Normal text extraction using `pypdf`
  * OCR fallback using `EasyOCR`
* AI-powered summarization using Groq API
* Streamlit frontend
* Downloadable generated notes
* Spinner/loading feedback
* Scrollable notes viewer

---

# Tech Stack

* Python
* Streamlit
* Groq API
* EasyOCR
* pdf2image
* pypdf

---

# Installation

Clone the repository:

```bash
git clone <your-repo-link>
cd <repo-name>
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_api_key_here
```

Get your free API key from Groq Cloud.

---

# Run the App

```bash
streamlit run app.py
```

---

# Recommended PDF Limits

For best performance:

* Use PDFs under ~100 pages
* Use clear scans/images
* English text recommended

---

# Project Structure

```text
.
├── app.py
├── main.py
├── requirements.txt
├── README.md
└── .env
```

---

# How It Works

1. User uploads a PDF
2. Text is extracted using `pypdf`
3. If extraction fails on a page:

   * OCR fallback is triggered using EasyOCR
4. Extracted text is sent to Groq API
5. AI generates:

   * Summary
   * Exam questions
   * Revision notes
   * Keywords
6. Results are displayed and downloadable

---

# Future Improvements

* Better prompt engineering
* Multi-language OCR support
* Chunked processing for huge PDFs
* Better UI/UX
* DOCX/PDF export support
* Authentication & cloud deployment

---

# License

MIT License
