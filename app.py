import os
import sqlite3
from flask import Flask, request, render_template, jsonify, send_file
from PyPDF2 import PdfReader
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize spaCy
nlp = spacy.load("en_core_web_sm")

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS job_descriptions
                 (id INTEGER PRIMARY KEY, description TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS analyses
                 (id INTEGER PRIMARY KEY, resume_text TEXT, match_score REAL,
                  missing_skills TEXT, job_desc_id INTEGER,
                  FOREIGN KEY(job_desc_id) REFERENCES job_descriptions(id))''')
    conn.commit()
    conn.close()

init_db()

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_keywords(text):
    doc = nlp(text)
    keywords = [token.text.lower() for token in doc if token.pos_ in ['NOUN', 'PROPN', 'ADJ'] and not token.is_stop]
    return set(keywords)

def calculate_match_score(resume_text, job_desc):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_desc])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(similarity * 100, 2)

def find_missing_skills(resume_keywords, job_keywords):
    return list(job_keywords - resume_keywords)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files or 'job_desc' not in request.form:
        return jsonify({'error': 'Missing resume or job description'}), 400
    
    resume_file = request.files['resume']
    job_desc = request.form['job_desc']
    
    if not resume_file.filename.endswith('.pdf'):
        return jsonify({'error': 'Please upload a PDF file'}), 400
    
    # Save job description to database
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    c.execute("INSERT INTO job_descriptions (description) VALUES (?)", (job_desc,))
    job_desc_id = c.lastrowid
    conn.commit()
    
    # Extract resume text
    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
    resume_file.save(resume_path)
    resume_text = extract_text_from_pdf(resume_path)
    
    # Extract keywords
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_desc)
    
    # Calculate match score
    match_score = calculate_match_score(resume_text, job_desc)
    
    # Find missing skills
    missing_skills = find_missing_skills(resume_keywords, job_keywords)
    
    # Save analysis to database
    c.execute("INSERT INTO analyses (resume_text, match_score, missing_skills, job_desc_id) VALUES (?, ?, ?, ?)",
              (resume_text, match_score, ', '.join(missing_skills), job_desc_id))
    analysis_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({
        'match_score': match_score,
        'missing_skills': missing_skills,
        'analysis_id': analysis_id
    })

@app.route('/download_report/<int:analysis_id>')
def download_report(analysis_id):
    conn = sqlite3.connect('resumes.db')
    c = conn.cursor()
    c.execute("SELECT match_score, missing_skills, job_desc_id FROM analyses WHERE id = ?", (analysis_id,))
    analysis = c.fetchone()
    
    if not analysis:
        conn.close()
        return "Analysis not found", 404
    
    c.execute("SELECT description FROM job_descriptions WHERE id = ?", (analysis[2],))
    job_desc = c.fetchone()[0]
    conn.close()
    
    match_score, missing_skills = analysis[0], analysis[1].split(', ') if analysis[1] else []
    
    # Generate PDF report
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, "Resume Analysis Report")
    p.drawString(100, 730, f"Match Score: {match_score}%")
    p.drawString(100, 710, "Missing Skills:")
    y = 690
    for skill in missing_skills:
        p.drawString(120, y, f"- {skill}")
        y -= 20
    p.showPage()
    p.save()
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=True, download_name='resume_analysis_report.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)