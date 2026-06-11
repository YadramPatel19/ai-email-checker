# 🏭 AI Email Content Checker — Tata Steel

An AI-powered multi-agent system that analyzes corporate emails before 
they are sent, checking for tone, compliance, clarity, grammar, and 
effectiveness. Built during my summer internship at Tata Steel.

## 🌐 Live Demo
👉 https://ai-email-checker-iy6rsrydb7qctkmufdaqky.streamlit.app

No installation needed — open in any browser!

## 🤖 Agents (8 total)

| Agent | Purpose |
|---|---|
| 🎭 Tone Analyzer | Checks professionalism and sentiment |
| 🛡️ Compliance Checker | Flags legal risks and data leaks |
| ✏️ Clarity Optimizer | Improves readability and structure |
| 📧 Subject Line Reviewer | Rates and suggests better subject lines |
| 🏆 Summary Agent | Final verdict and action plan |
| ✍️ Email Rewriter | Rewrites full email fixing all issues |
| 📝 Grammar Checker | Sentence-level corrections with explanations |
| 🔁 Duplicate Detector | Detects repetitive and redundant content |

## ✨ Features

- 📎 File uploads — PDF, Word (.docx), Excel (.xlsx), Images, GIFs
- 🔍 OCR — extracts text from images and GIFs using Tesseract
- 🔗 Hyperlink verification — checks working and broken links
- 🔲 QR code detection — extracts and verifies URLs inside QR codes
- 😊 Emoji detection — flags inappropriate emoji usage
- 📊 Overall score out of 100 with verdict
- 🔄 Before vs After email comparison
- 📋 Grammar corrections table (Original / Correction / Explanation)
- 🖼️ Image alt text suggestions
- 💬 User feedback mechanism
- ⬇️ Export reports as PDF, Word, or TXT
- 💾 Auto-saves all analysis reports locally

## 🚀 How to run

### Live demo (recommended)
Open directly in browser — no setup needed:
👉 https://ai-email-checker-iy6rsrydb7qctkmufdaqky.streamlit.app

### Run locally

```bash
git clone https://github.com/YadramPatel19/ai-email-checker.git
cd ai-email-checker
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:
__API_KEY=your_key_here

Run web UI:
```bash
streamlit run app.py
```

Run terminal version:
```bash
python main.py
```

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3 | Core language |
| Groq API — Llama 3.3 70B | AI model (free tier) |
| Streamlit | Web UI framework |
| Tesseract OCR | Text extraction from images |
| PyMuPDF | PDF text extraction |
| python-docx | Word document handling |
| openpyxl | Excel file handling |
| pyzbar + OpenCV | QR code detection |
| FPDF2 | PDF report generation |
| Multi-Agent Architecture | Orchestrated AI pipeline |
| Streamlit Cloud | Free cloud deployment |

## 📁 Project structure
├── app.py             # Streamlit web UI (main interface)
├── agents.py          # All 6 AI agents + orchestrator
├── grammar_agent.py   # Grammar checker + duplicate detector
├── extractor.py       # File reading, OCR, QR code detection
├── export_report.py   # PDF and Word report generation
├── utils.py           # Groq API connection
├── main.py            # Terminal version
├── packages.txt       # System dependencies for cloud
├── requirements.txt   # Python dependencies
├── reports/           # Auto-generated analysis reports
└── .env               # API key (never uploaded to GitHub)

## 📋 Supported Input Types

- ✅ Plain text email body
- ✅ PDF files (multiple)
- ✅ Word documents (.docx)
- ✅ Excel files (.xlsx)
- ✅ Images (.png, .jpg, .jpeg)
- ✅ GIF files
- ✅ Hyperlinks (auto-detected and verified)
- ✅ QR codes (extracted from images)
- ✅ Emojis (detected and flagged)

## 👨‍💻 Built by

**Yadram Patel** — Summer Intern, Tata Steel, 2026