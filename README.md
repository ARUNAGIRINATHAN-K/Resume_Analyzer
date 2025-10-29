## Resume Job Fit Analyzer

A sophisticated web-based Resume Analyzer that uses Natural Language Processing (NLP) to compare resumes with job descriptions and provides compatibility scores with actionable improvement suggestions.

![Resume Analyzer Screenshot](https://img.shields.io/badge/Python-3.11-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.0-green.svg)
![spaCy](https://img.shields.io/badge/spaCy-3.8.0-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Features

- **PDF Resume Upload**: Extract text from PDF resumes using PyMuPDF
- **NLP-Powered Analysis**: Advanced text processing using spaCy for skill extraction and analysis
- **Intelligent Scoring System**: Weighted scoring algorithm considering:
  - Skills overlap (50% weight)
  - Role relevance (30% weight)
  - Experience/education match (20% weight)
- **Visual Analytics**: Interactive charts powered by Chart.js
- **Keyword Analysis**: Identify matched and missing keywords between resume and job description
- **Actionable Suggestions**: Get personalized recommendations to improve resume alignment
- **Responsive Design**: Clean, modern UI with Bootstrap framework
- **Real-time Processing**: Fast analysis with detailed progress indicators

## Demo

Upload your resume and paste a job description to get:
- Overall compatibility score (0-100)
- Detailed breakdown by category
- Matched vs. missing skills visualization
- Prioritized improvement suggestions

## Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/ARUNAGIRINATHAN-K/resume-analyzer.git
   cd resume-analyzer
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy language model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Set environment variables**
   ```bash
   export SESSION_SECRET="your-secret-key-here"
   ```
   Or create a `.env` file:
   ```
   SESSION_SECRET=your-secret-key-here
   ```

6. **Run the application**
   ```bash
   python main.py
   ```

7. **Open your browser**
   Navigate to `http://localhost:5000`

## Project Structure

```
resume-analyzer/
├── app.py                 # Main Flask application
├── main.py               # Application entry point
├── nlp_processor.py      # NLP processing and text analysis
├── scoring_engine.py     # Scoring algorithms and suggestions
├── requirements.txt      # Python dependencies
├── templates/           # HTML templates
│   ├── base.html        # Base template with Bootstrap
│   ├── index.html       # Upload form
│   └── results.html     # Analysis results
├── static/              # Static assets
│   ├── css/
│   │   └── style.css    # Custom styling
│   └── js/
│       └── main.js      # Frontend interactions
└── uploads/             # Temporary file storage (auto-created)
```

## Technology Stack

### Backend
- **Flask**: Lightweight web framework
- **spaCy**: Industrial-strength NLP library
- **scikit-learn**: Machine learning for TF-IDF and similarity calculations
- **PyMuPDF**: PDF text extraction
- **NumPy**: Numerical computations

### Frontend
- **Bootstrap 5**: Responsive UI framework
- **Chart.js**: Interactive data visualizations
- **Font Awesome**: Icon library
- **Vanilla JavaScript**: Enhanced user interactions

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main upload form |
| `/analyze` | POST | Process resume and job description |

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SESSION_SECRET` | Flask secret key for sessions | Required |
| `UPLOAD_FOLDER` | Directory for temporary files | `uploads` |
| `MAX_CONTENT_LENGTH` | Maximum file size | `16MB` |

### Supported File Types

- PDF files only
- Maximum size: 16MB
- Text-based PDFs (not scanned images)

## Scoring Algorithm

The compatibility score is calculated using a weighted approach:

1. **Skills Match (50%)**: Overlap between resume skills and job requirements
2. **Role Relevance (30%)**: Alignment of job titles and responsibilities
3. **Experience Level (20%)**: Years of experience and education level match

### Score Interpretation

- **85-100**: Excellent match - Strong alignment with position
- **70-84**: Good match - Minor improvements recommended
- **50-69**: Moderate match - Targeted resume updates needed
- **0-49**: Low match - Significant changes required

## Development

### Running in Development Mode

```bash
flask --app app run --host=0.0.0.0 --port=5000 --debug
```

### VS Code Setup

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Flask App",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal",
            "env": {
                "SESSION_SECRET": "dev-secret-key"
            }
        }
    ]
}
```

### Adding New Skills

Edit `nlp_processor.py` to add new skill categories:

```python
self.skill_patterns = {
    'programming': ['python', 'java', 'javascript', ...],
    'web': ['html', 'css', 'react', ...],
    'your_category': ['skill1', 'skill2', ...]
}
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add tests for new features
- Update documentation for API changes
- Ensure cross-browser compatibility

## Deployment

### Production Deployment

```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

### Docker Support

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY . .
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

## Security Considerations

- File uploads are validated for type and size
- Temporary files are automatically cleaned up
- CSRF protection enabled
- Secure filename handling
- Environment-based configuration

## Performance

- Average processing time: 2-5 seconds per resume
- Supports files up to 16MB
- Memory-efficient text processing
- Optimized keyword extraction algorithms

## Troubleshooting

### Common Issues

**spaCy model not found**
```bash
python -m spacy download en_core_web_sm
```

**PDF text extraction fails**
- Ensure PDF is text-based (not scanned image)
- Check file size under 16MB limit
- Verify PDF is not password protected

**Low accuracy scores**
- Use detailed job descriptions
- Include complete resume content
- Ensure proper formatting in both documents

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [spaCy](https://spacy.io/) for excellent NLP capabilities
- [scikit-learn](https://scikit-learn.org/) for machine learning tools
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Bootstrap](https://getbootstrap.com/) for responsive design
- [Chart.js](https://www.chartjs.org/) for data visualization


**⭐ Star this repository if you find it helpful!**
