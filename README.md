# 🏭 AI Email Content Checker — Tata Steel

An AI-powered multi-agent system to analyze corporate emails 
before they are sent. Built during my summer internship at Tata Steel.

## 🤖 Agents
| Agent | Purpose |
|---|---|
| 🎭 Tone Analyzer | Checks professionalism and sentiment |
| 🛡️ Compliance Checker | Flags legal risks and data leaks |
| ✏️ Clarity Optimizer | Improves readability and structure |
| 📧 Subject Line Reviewer | Rates and suggests better subject lines |
| 🏆 Summary Agent | Final verdict and action plan |

## 🚀 How to run

### Terminal version
    python main.py

### Web UI version
    streamlit run app.py

## ⚙️ Setup

    git clone https://github.com/YOUR_USERNAME/ai-email-checker-tata-steel.git
    cd ai-email-checker-tata-steel
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt

Create a `.env` file:

    GROQ_API_KEY=your_key_here

## 🛠️ Tech Stack
- Python 3
- Groq API — Llama 3.3 70B (free tier)
- Streamlit (web UI)
- Multi-agent architecture

## 📁 Project structure
    ├── main.py        # Terminal app + report saving
    ├── agents.py      # All 5 AI agents + orchestrator
    ├── utils.py       # Groq API connection
    ├── app.py         # Streamlit web UI
    ├── reports/       # Auto-generated analysis reports
    └── .env           # API key (not uploaded)

## 👨‍💻 Built by
YADRAM PATEL — Summer Intern, Tata Steel, 2026