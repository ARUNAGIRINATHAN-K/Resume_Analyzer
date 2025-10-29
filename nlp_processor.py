import spacy
import re
import logging
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class NLPProcessor:
    """Handles NLP processing for resume and job description analysis."""
    
    def __init__(self):
        """Initialize the NLP processor with spaCy model."""
        try:
            self.nlp = spacy.load("en_core_web_sm")
            logging.info("spaCy model loaded successfully")
        except OSError:
            logging.error("spaCy model 'en_core_web_sm' not found. Please install it with: python -m spacy download en_core_web_sm")
            raise
        
        # Define skill categories and common terms
        self.skill_patterns = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'swift', 'kotlin', 'scala', 'r'],
            'web': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'oracle', 'sqlite', 'redis', 'elasticsearch'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins'],
            'data': ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'tableau', 'power bi'],
            'tools': ['git', 'jira', 'confluence', 'slack', 'trello', 'notion']
        }
        
        self.experience_patterns = [
            r'(\d+)[\+\-\s]*(?:to|\-|–)?\s*(\d+)?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(\d+)[\+\-\s]*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(\d+)[\+\-\s]*(?:to|\-|–)?\s*(\d+)?\s*(?:years?|yrs?)'
        ]
        
        self.education_keywords = [
            'bachelor', 'master', 'phd', 'degree', 'university', 'college', 'education',
            'computer science', 'engineering', 'business', 'mba', 'certification'
        ]

    def clean_text(self, text):
        """Clean and preprocess text."""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        text = text.strip().lower()
        return text

    def extract_skills(self, text):
        """Extract skills from text using pattern matching and NLP."""
        text_lower = text.lower()
        found_skills = []
        
        # Extract using predefined skill patterns
        for category, skills in self.skill_patterns.items():
            for skill in skills:
                if skill in text_lower:
                    found_skills.append(skill)
        
        # Use spaCy to find additional technical terms
        doc = self.nlp(text)
        for token in doc:
            # Look for capitalized technical terms (likely technologies/tools)
            if (token.text.isupper() and len(token.text) > 2 and token.pos_ in ['NOUN', 'PROPN']) or \
               (token.like_url or token.text.endswith('.js') or token.text.endswith('.py')):
                found_skills.append(token.text.lower())
        
        return list(set(found_skills))

    def extract_experience_years(self, text):
        """Extract years of experience from text."""
        years = []
        text_lower = text.lower()
        
        for pattern in self.experience_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    # Handle range patterns
                    for year in match:
                        if year and year.isdigit():
                            years.append(int(year))
                else:
                    if match.isdigit():
                        years.append(int(match))
        
        return max(years) if years else 0

    def extract_education_level(self, text):
        """Extract education level from text."""
        text_lower = text.lower()
        education_score = 0
        
        if 'phd' in text_lower or 'doctorate' in text_lower:
            education_score = 4
        elif 'master' in text_lower or 'mba' in text_lower:
            education_score = 3
        elif 'bachelor' in text_lower:
            education_score = 2
        elif any(keyword in text_lower for keyword in ['degree', 'university', 'college']):
            education_score = 1
        
        return education_score

    def extract_job_roles(self, text):
        """Extract job roles and titles from text."""
        doc = self.nlp(text)
        roles = []
        
        # Common job title patterns
        job_patterns = [
            r'(?:senior|junior|lead|principal|staff)?\s*(?:software|web|data|machine learning|ai|backend|frontend|full[\-\s]?stack)?\s*(?:engineer|developer|analyst|scientist|architect|manager|director)',
            r'(?:product|project|program)\s*manager',
            r'(?:data|business|financial|marketing)\s*analyst',
            r'(?:ui|ux|graphic)\s*designer'
        ]
        
        text_lower = text.lower()
        for pattern in job_patterns:
            matches = re.findall(pattern, text_lower)
            roles.extend(matches)
        
        # Use NLP to find job-related entities
        for ent in doc.ents:
            if ent.label_ in ['PERSON', 'ORG'] and any(keyword in ent.text.lower() for keyword in ['engineer', 'developer', 'manager', 'analyst']):
                roles.append(ent.text.lower())
        
        return list(set(roles))

    def extract_keywords(self, text, top_n=50):
        """Extract important keywords using TF-IDF."""
        # Clean text
        cleaned_text = self.clean_text(text)
        
        # Use TF-IDF to extract keywords
        vectorizer = TfidfVectorizer(
            max_features=top_n,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95
        )
        
        try:
            tfidf_matrix = vectorizer.fit_transform([cleaned_text])
            feature_names = vectorizer.get_feature_names_out()
            scores = tfidf_matrix.toarray()[0]
            
            # Get keywords with scores
            keyword_scores = list(zip(feature_names, scores))
            keyword_scores.sort(key=lambda x: x[1], reverse=True)
            
            return [keyword for keyword, score in keyword_scores if score > 0]
        except ValueError:
            # Handle case where text is too short for TF-IDF
            doc = self.nlp(cleaned_text)
            return [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and len(token.text) > 2]

    def analyze_text(self, text, text_type='general'):
        """Perform comprehensive analysis of the text."""
        if not text or not text.strip():
            return {
                'skills': [],
                'experience_years': 0,
                'education_level': 0,
                'job_roles': [],
                'keywords': [],
                'word_count': 0,
                'sentence_count': 0
            }
        
        # Basic text statistics
        doc = self.nlp(text)
        word_count = len([token for token in doc if not token.is_space])
        sentence_count = len(list(doc.sents))
        
        # Extract various components
        skills = self.extract_skills(text)
        experience_years = self.extract_experience_years(text)
        education_level = self.extract_education_level(text)
        job_roles = self.extract_job_roles(text)
        keywords = self.extract_keywords(text)
        
        logging.debug(f"Analyzed {text_type}: {len(skills)} skills, {experience_years} years exp, {len(keywords)} keywords")
        
        return {
            'skills': skills,
            'experience_years': experience_years,
            'education_level': education_level,
            'job_roles': job_roles,
            'keywords': keywords,
            'word_count': word_count,
            'sentence_count': sentence_count,
            'text_type': text_type
        }

    def calculate_text_similarity(self, text1, text2):
        """Calculate similarity between two texts using TF-IDF and cosine similarity."""
        try:
            vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return similarity
        except:
            return 0.0
