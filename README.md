# 🎯 ResumeFit (Resume Job Fit Analyzer)

AI-powered resume analyzer using NLP to compare resumes against job descriptions, calculate compatibility scores, identify skill gaps, and provide actionable resume enhancement suggestions.

---

## ✨ Features

- **Semantic NLP Parsing**: Uses spaCy (`en_core_web_sm`) and TF-IDF extraction for tokenization, skill mapping, and description alignment.
- **Weighted Compatibility Score**: Calculates an overall match score out of 100 based on:
  - **Skills Match (50%)**: Identifies overlapping technical and soft skills.
  - **Role Relevance (30%)**: Matches experience descriptions and job titles.
  - **Experience Level (20%)**: Compares years of experience and education requirements.
- **Real-Time Interactive Optimizer**: Features an in-browser split-view text editor allowing you to re-tune and re-analyze your resume instantly without page reloads.
- **Actionable Gap Analysis**: Suggests missing keywords categorized by priority level (High, Medium, Low).
- **Responsive Dashboard**: Dark glassmorphic user interface built with Bootstrap 5 and Chart.js.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip

### 1. Clone & Set Up
```bash
git clone https://github.com/ARUNAGIRINATHAN-K/resume-analyzer.git
cd resume-analyzer

# Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Download the spaCy pipeline model
python -m spacy download en_core_web_sm
```

### 2. Configure Environment
Create a `.env` file at the root:
```env
SESSION_SECRET=your-secure-session-key
FLASK_ENV=development
PORT=5000
```

### 3. Run the Server
```bash
python wsgi.py
```
Open **`http://localhost:5000`** in your browser.

---

## 🐳 Docker Deployment

To build and run the application inside a container:

### Using Docker Compose
```bash
docker compose up --build
```

### Or using Standalone Docker commands
```bash
docker build -t resume-analyzer .
docker run -p 5000:5000 resume-analyzer
```

---

## 🧪 Testing

Run the automated test suite:
```bash
pytest
```

---

## 📁 Project Structure

```
resume-analyzer/
├── app/                  # Application Package
│   ├── __init__.py       # Application Factory
│   ├── config.py         # Configuration Rules
│   ├── routes.py         # Views & API Endpoints
│   ├── utils.py          # PDF Extraction Helpers
│   ├── nlp_processor.py  # spaCy NLP processing logic
│   ├── scoring_engine.py # Scoring algorithms & suggestions
│   ├── static/           # UI Stylesheets & Scripts
│   └── templates/        # HTML Layouts & Views
├── tests/                # Automated Test Suite
├── wsgi.py               # Production Entrypoint
├── Dockerfile            # Container Builder
├── docker-compose.yml    # Orchestration Settings
├── requirements.txt      # Dependencies
└── .env.example          # Sample configurations
```

---
**Made by [ARUNAGIRINATHAN K](https://github.com/ARUNAGIRINATHAN-K)**
