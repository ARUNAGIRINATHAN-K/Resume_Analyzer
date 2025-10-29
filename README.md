# Resume Job Fit Analyzer 🎯

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.0-green.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![spaCy](https://img.shields.io/badge/spaCy-3.8.0-orange.svg?logo=spacy&logoColor=white)](https://spacy.io/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Chart.js](https://img.shields.io/badge/Chart.js-4.0+-red.svg?logo=chart.js&logoColor=white)](https://www.chartjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg)](https://github.com/ARUNAGIRINATHAN-K/resume-analyzer/graphs/commit-activity)
[![Code Style](https://img.shields.io/badge/code%20style-PEP8-blue.svg)](https://www.python.org/dev/peps/pep-0008/)

> A sophisticated web-based Resume Analyzer powered by Natural Language Processing (NLP) that intelligently compares resumes with job descriptions, providing detailed compatibility scores and actionable improvement suggestions in real-time.

![Resume Analyzer Demo](static/img/demo.gif)

## ✨ Key Features

### 📊 Smart Analysis
- **PDF Resume Upload**: Seamless text extraction from PDF resumes using PyMuPDF
- **NLP-Powered Analysis**: State-of-the-art text processing with spaCy for accurate skill extraction
- **Real-time Processing**: Lightning-fast analysis with live progress indicators

### 🎯 Intelligent Scoring
- **Comprehensive Scoring Algorithm**:
  - 📈 Skills Match (50%): Technical and soft skills alignment
  - 👔 Role Relevance (30%): Job title and responsibility matching
  - 🎓 Experience/Education (20%): Qualifications assessment
- **Dynamic Keyword Analysis**: Smart identification of matching and missing keywords

### 📱 Modern User Interface
- **Responsive Design**: Clean, modern UI powered by Bootstrap 5
- **Interactive Visualizations**: Dynamic charts and graphs using Chart.js
- **Drag & Drop**: Intuitive file upload experience
- **Dark Mode Support**: Eye-friendly interface options

### 🤖 Smart Recommendations
- **Personalized Suggestions**: AI-driven resume improvement tips
- **Skill Gap Analysis**: Detailed breakdown of missing qualifications
- **Priority Insights**: Focus areas for maximum impact

## Demo

Upload your resume and paste a job description to get:
- Overall compatibility score (0-100)
- Detailed breakdown by category
- Matched vs. missing skills visualization
- Prioritized improvement suggestions

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:
- [![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python&logoColor=white)](https://www.python.org/downloads/)
- [![pip](https://img.shields.io/badge/pip-latest-blue.svg?logo=pypi&logoColor=white)](https://pip.pypa.io/en/stable/installation/)
- [![Git](https://img.shields.io/badge/Git-required-red.svg?logo=git&logoColor=white)](https://git-scm.com/downloads)

### 📥 Installation

1. **Clone the Repository**
   ```powershell
   git clone https://github.com/ARUNAGIRINATHAN-K/resume-analyzer.git
   cd resume-analyzer
   ```

2. **Set Up Virtual Environment**
   ```powershell
   # Create a new virtual environment
   python -m venv venv

   # Activate the virtual environment
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   # source venv/bin/activate
   ```

3. **Install Dependencies**
   ```powershell
   # Upgrade pip to latest version
   python -m pip install --upgrade pip

   # Install project dependencies
   pip install -r requirements.txt
   ```

4. **Install NLP Model**
   ```powershell
   # Download and install spaCy language model
   python -m spacy download en_core_web_sm
   ```

### 🔧 Configuration

1. **Environment Setup**
   Create a `.env` file in the project root:
   ```env
   SESSION_SECRET=your-secret-key-here
   UPLOAD_FOLDER=uploads
   MAX_CONTENT_LENGTH=16777216  # 16MB in bytes
   DEBUG=False
   ```

2. **Initialize Database**
   ```powershell
   # Create required directories
   mkdir uploads
   ```

### 🏃‍♂️ Run the Application

1. **Development Mode**
   ```powershell
   python main.py
   ```

2. **Production Mode**
   ```powershell
   gunicorn --bind 0.0.0.0:5000 main:app
   ```

3. **Access the Application**
   Open your browser and navigate to:
   - Local: http://localhost:5000
   - Network: http://your-ip:5000

### 🐳 Docker Support

```powershell
# Build the Docker image
docker build -t resume-analyzer .

# Run the container
docker run -p 5000:5000 resume-analyzer
```

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

## 🛠️ Technology Stack

### 🐍 Backend Framework
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.0-green.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-20.1-black.svg?style=for-the-badge&logo=gunicorn&logoColor=white)](https://gunicorn.org/)

### 🧠 AI & Data Processing
[![spaCy](https://img.shields.io/badge/spaCy-3.8.0-blue.svg?style=for-the-badge&logo=spacy&logoColor=white)](https://spacy.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-orange.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.24-013243.svg?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![PyMuPDF](https://img.shields.io/badge/PyMuPDF-1.23-red.svg?style=for-the-badge)](https://pymupdf.readthedocs.io/)

### 🎨 Frontend Technologies
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Chart.js](https://img.shields.io/badge/Chart.js-4.0-red.svg?style=for-the-badge&logo=chart.js&logoColor=white)](https://www.chartjs.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg?style=for-the-badge&logo=javascript&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Font Awesome](https://img.shields.io/badge/Font_Awesome-6.0-339AF0.svg?style=for-the-badge&logo=font-awesome&logoColor=white)](https://fontawesome.com/)

### 🔧 Development & Deployment
[![Docker](https://img.shields.io/badge/Docker-20.10+-blue.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Git](https://img.shields.io/badge/Git-2.x-red.svg?style=for-the-badge&logo=git&logoColor=white)](https://git-scm.com/)
[![VS Code](https://img.shields.io/badge/VS_Code-Latest-007ACC.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)](https://code.visualstudio.com/)

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
