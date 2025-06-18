## AI Resume Analyzer

A web application that analyzes resumes by extracting keywords, matching them against a job description, and providing<br>
a match score, missing skills, and a downloadable feedback report. Built with Flask, spaCy, scikit-learn, and SQLite,<br>
it features a modern dark-themed UI for an enhanced user experience.

**Table of Contents**

>Features

>Technologies

>Project Structure

>Installation

>Usage

>Contributing



## Features

>**Resume Upload**: Upload PDF resumes for analysis.

>Keyword Extraction: Extracts relevant keywords from resumes and job descriptions using spaCy.

>Job Description Matching: Calculates a match score between the resume and job description using TF-IDF and cosine similarity.

>Missing Skills Identification: Highlights skills present in the job description but missing from the resume.

>Feedback Report: Generates a downloadable PDF report summarizing the match score and missing skills.

>Modern UI: Responsive dark-themed interface with user-friendly form and visual feedback.

>Persistent Storage: Stores job descriptions and analysis results in an SQLite database.

## Technologies

>Frontend: HTML, CSS, JavaScript

>Backend: Flask (Python)

>ML/NLP: spaCy, scikit-learn

>Database: SQLite

>PDF Processing: PyPDF2 (for resume parsing), ReportLab (for report generation)

>Styling: Custom CSS with Inter font from Google Fonts

**Project Structure**
```
resume_analyzer/
├── app.py                  # Main Flask application
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
├── resumes.db              # SQLite database (auto-generated)
├── static/                 # Static assets
│   ├── script.js           # JavaScript for form handling
│   └── style.css           # CSS for dark-themed UI
├── templates/              # HTML templates
│   └── index.html          # Main page template
└── uploads/                # Directory for uploaded resumes
```

**Install dependencies:**
```
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**Run the application:**
```
python app.py
```

>Access the app at http://localhost:5000.



**Usage**

>Open the app: Navigate to http://localhost:5000 in your browser.

>Upload a resume: Select a PDF resume file using the file upload input.

>Enter a job description: Paste or type the job description in the textarea.

>Analyze: Click the "Analyze Resume" button to process the resume.

>View results: See the match score, missing skills, and a link to download a PDF report.

>Download report: Click the "Download Report" link to save the analysis as a PDF.


