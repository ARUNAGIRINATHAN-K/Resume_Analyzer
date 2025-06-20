import os
import sqlite3
import logging
from flask import Flask, request, render_template, jsonify, send_file
from PyPDF2 import PdfReader
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize spaCy
nlp = spacy.load("en_core_web_sm")

# Initialize and migrate SQLite database
def init_db():
    try:
        conn = sqlite3.connect('resumes.db')
        c = conn.cursor()
        # Create job_descriptions table
        c.execute('''CREATE TABLE IF NOT EXISTS job_descriptions
                     (id INTEGER PRIMARY KEY, description TEXT)''')
        # Create analyses table with initial schema
        c.execute('''CREATE TABLE IF NOT EXISTS analyses
                     (id INTEGER PRIMARY KEY, resume_text TEXT, match_score REAL,
                      missing_skills TEXT, job_desc_id INTEGER,
                      FOREIGN KEY(job_desc_id) REFERENCES job_descriptions(id))''')
        conn.commit()
        
        # Check for missing columns and add them
        c.execute("PRAGMA table_info(analyses)")
        columns = [col[1] for col in c.fetchall()]
        new_columns = [
            ('education_score', 'REAL'),
            ('technical_score', 'REAL'),
            ('expectation_score', 'REAL')
        ]
        for col_name, col_type in new_columns:
            if col_name not in columns:
                c.execute(f"ALTER TABLE analyses ADD COLUMN {col_name} {col_type}")
                logger.info(f"Added column {col_name} to analyses table")
        conn.commit()
        logger.info("Database initialized and migrated successfully")
    except Exception as e:
        logger.error(f"Database initialization/migration failed: {str(e)}")
        raise
    finally:
        conn.close()

init_db()

def extract_text_from_pdf(pdf_file):
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        logger.info("PDF text extracted successfully")
        return text
    except Exception as e:
        logger.error(f"PDF extraction failed: {str(e)}")
        raise

def extract_keywords(text, pos_tags=['NOUN', 'PROPN', 'ADJ']):
    doc = nlp(text)
    keywords = [token.text.lower() for token in doc if token.pos_ in pos_tags and not token.is_stop]
    return set(keywords)

def extract_education(text):
    doc = nlp(text)
    education_keywords = {'bachelor', 'master', 'phd', 'degree', 'university', 'college', 'education'}
    education = [ent.text.lower() for ent in doc.ents if ent.label_ in ['ORG', 'GPE'] or any(kw in ent.text.lower() for kw in education_keywords)]
    return set(education)

def extract_technical_skills(text):
    doc = nlp(text)
    tech_keywords = {'python', 'java', 'javascript', 'sql', 'machine learning', 'data analysis', 'cloud', 'aws', 'docker'}
    skills = [token.text.lower() for token in doc if token.pos_ in ['NOUN', 'PROPN'] and (token.text.lower() in tech_keywords or token.text.lower().endswith('ing'))]
    return set(skills)

def calculate_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(similarity * 100, 2)

def calculate_composite_score(education_score, technical_score, expectation_score):
    return round(0.2 * education_score + 0.5 * technical_score + 0.3 * expectation_score, 2)

def find_missing_skills(resume_keywords, job_keywords):
    return list(job_keywords - resume_keywords)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    try:
        if 'resume' not in request.files or 'job_desc' not in request.form:
            logger.warning("Missing resume or job description in request")
            return jsonify({'error': 'Please provide both a resume file and a job description'}), 400
        
        resume_file = request.files['resume']
        job_desc = request.form['job_desc']
        
        if not resume_file.filename:
            logger.warning("No file selected for upload")
            return jsonify({'error': 'No file selected'}), 400
        
        if not resume_file.filename.endswith('.pdf'):
            logger.warning(f"Invalid file type: {resume_file.filename}")
            return jsonify({'error': 'Please upload a PDF file'}), 400
        
        # Check file size
        resume_file.seek(0, os.SEEK_END)
        file_size = resume_file.tell()
        if file_size > app.config['MAX_CONTENT_LENGTH']:
            logger.warning(f"File too large: {file_size} bytes")
            return jsonify({'error': f'File size exceeds {app.config["MAX_CONTENT_LENGTH"] // (1024 * 1024)}MB limit'}), 400
        resume_file.seek(0)
        
        # Save job description to database
        conn = sqlite3.connect('resumes.db')
        c = conn.cursor()
        c.execute("INSERT INTO job_descriptions (description) VALUES (?)", (job_desc,))
        job_desc_id = c.lastrowid
        conn.commit()
        
        # Extract resume text
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
        try:
            resume_file.save(resume_path)
            resume_text = extract_text_from_pdf(resume_path)
        except Exception as e:
            logger.error(f"Failed to save or process PDF: {str(e)}")
            conn.close()
            return jsonify({'error': 'Failed to process PDF file'}), 500
        
        # Extract keywords
        resume_keywords = extract_keywords(resume_text)
        job_keywords = extract_keywords(job_desc)
        
        # Calculate overall match score
        match_score = calculate_similarity(resume_text, job_desc)
        
        # Calculate criteria-specific scores
        resume_education = extract_education(resume_text)
        job_education = extract_education(job_desc)
        education_score = calculate_similarity(' '.join(resume_education), ' '.join(job_education)) if resume_education and job_education else 50.0
        
        resume_skills = extract_technical_skills(resume_text)
        job_skills = extract_technical_skills(job_desc)
        technical_score = calculate_similarity(' '.join(resume_skills), ' '.join(job_skills)) if resume_skills and job_skills else 50.0
        
        expectation_score = match_score
        
        # Composite score
        composite_score = calculate_composite_score(education_score, technical_score, expectation_score)
        
        # Find missing skills
        missing_skills = find_missing_skills(resume_keywords, job_keywords)
        
        # Save analysis to database
        c.execute('''INSERT INTO analyses (resume_text, match_score, missing_skills, job_desc_id,
                     education_score, technical_score, expectation_score)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (resume_text, composite_score, ', '.join(missing_skills), job_desc_id,
                   education_score, technical_score, expectation_score))
        analysis_id = c.lastrowid
        conn.commit()
        conn.close()
        logger.info(f"Analysis completed: ID {analysis_id}, Score {composite_score}")
        
        # Prepare evaluation table data
        evaluation_table = [
            {
                'criteria': 'Education Fit',
                'description': 'Alignment of educational qualifications with job requirements.',
                'expected': ' '.join(job_education) or 'Relevant degree or certification',
                'resume': ' '.join(resume_education) or 'No education details found',
                'score': education_score
            },
            {
                'criteria': 'Technical Skills',
                'description': 'Possession of technical skills required for the role.',
                'expected': ' '.join(job_skills) or 'Specific technical expertise',
                'resume': ' '.join(resume_skills) or 'No technical skills found',
                'score': technical_score
            },
            {
                'criteria': 'Job Expectation Fit',
                'description': 'Overall alignment with job responsibilities and expectations.',
                'expected': 'Keywords matching job duties and qualifications',
                'resume': 'Keywords from resume',
                'score': expectation_score
            }
        ]
        
        return jsonify({
            'match_score': composite_score,
            'missing_skills': missing_skills,
            'analysis_id': analysis_id,
            'evaluation_table': evaluation_table
        })
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred. Please try again.'}), 500

@app.route('/download_report/<int:analysis_id>')
def download_report(analysis_id):
    try:
        conn = sqlite3.connect('resumes.db')
        c = conn.cursor()
        c.execute('''SELECT match_score, missing_skills, job_desc_id, education_score,
                     technical_score, expectation_score FROM analyses WHERE id = ?''', (analysis_id,))
        analysis = c.fetchone()
        
        if not analysis:
            logger.warning(f"Analysis not found: ID {analysis_id}")
            conn.close()
            return "Analysis not found", 404
        
        c.execute("SELECT description FROM job_descriptions WHERE id = ?", (analysis[2],))
        job_desc = c.fetchone()[0]
        conn.close()
        
        match_score, missing_skills, education_score, technical_score, expectation_score = analysis[0], analysis[1].split(', ') if analysis[1] else [], analysis[3], analysis[4], analysis[5]
        
        # Generate PDF report
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 750, "Resume Analysis Report")
        
        p.setFont("Helvetica", 12)
        p.drawString(100, 730, f"Composite Match Score: {match_score}%")
        p.drawString(100, 710, "Missing Skills:")
        y = 690
        for skill in missing_skills:
            p.drawString(120, y, f"- {skill}")
            y -= 20
        
        p.drawString(100, y - 20, "Evaluation Summary:")
        y -= 40
        p.setFont("Helvetica-Bold", 10)
        p.drawString(100, y, "Criteria")
        p.drawString(200, y, "Expected")
        p.drawString(350, y, "Your Resume")
        p.drawString(500, y, "Score")
        p.setFont("Helvetica", 10)
        y -= 20
        
        evaluation_table = [
            {'criteria': 'Education Fit', 'expected': extract_education(job_desc), 'resume': extract_education(resume_text), 'score': education_score},
            {'criteria': 'Technical Skills', 'expected': extract_technical_skills(job_desc), 'resume': extract_technical_skills(resume_text), 'score': technical_score},
            {'criteria': 'Job Expectation Fit', 'expected': 'Job duties alignment', 'resume': 'Resume keywords', 'score': expectation_score}
        ]
        
        for row in evaluation_table:
            p.drawString(100, y, row['criteria'])
            p.drawString(200, y, ' '.join(row['expected'])[:20] + '...' if row['expected'] else 'N/A')
            p.drawString(350, y, ' '.join(row['resume'])[:20] + '...' if row['resume'] else 'N/A')
            p.drawString(500, y, f"{row['score']}%")
            y -= 20
        
        p.showPage()
        p.save()
        buffer.seek(0)
        logger.info(f"Generated PDF report for analysis ID {analysis_id}")
        
        return send_file(buffer, as_attachment=True, download_name='resume_analysis_report.pdf', mimetype='application/pdf')
    except Exception as e:
        logger.error(f"Download report error: {str(e)}")
        return jsonify({'error': 'Failed to generate report'}), 500

if __name__ == '__main__':
    app.run(debug=True)