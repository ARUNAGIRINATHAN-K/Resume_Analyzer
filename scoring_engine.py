import logging
from collections import Counter
import numpy as np

class ScoringEngine:
    """Handles scoring logic for job fit analysis."""
    
    def __init__(self):
        """Initialize scoring weights and thresholds."""
        self.weights = {
            'skills': 0.5,      # 50% weight for skill overlap
            'role': 0.3,        # 30% weight for role relevance
            'experience': 0.2   # 20% weight for experience/education match
        }
        
        # Scoring thresholds
        self.skill_match_threshold = 0.3  # Minimum skill overlap for good score
        self.role_match_threshold = 0.2   # Minimum role overlap for good score
        
    def calculate_skill_overlap_score(self, resume_skills, jd_skills):
        """Calculate skill overlap score between resume and job description."""
        if not jd_skills:
            return 0, [], []
        
        resume_skills_set = set(skill.lower() for skill in resume_skills)
        jd_skills_set = set(skill.lower() for skill in jd_skills)
        
        # Find matches and missing skills
        matched_skills = list(resume_skills_set.intersection(jd_skills_set))
        missing_skills = list(jd_skills_set - resume_skills_set)
        
        # Calculate overlap percentage
        overlap_ratio = len(matched_skills) / len(jd_skills_set) if jd_skills_set else 0
        
        # Convert to 0-100 score with some normalization
        skill_score = min(100, overlap_ratio * 150)  # Boost to make scoring more generous
        
        return skill_score, matched_skills, missing_skills
    
    def calculate_role_relevance_score(self, resume_roles, jd_roles):
        """Calculate role relevance score."""
        if not jd_roles:
            return 50  # Default neutral score if no roles detected
        
        resume_roles_set = set(role.lower() for role in resume_roles)
        jd_roles_set = set(role.lower() for role in jd_roles)
        
        # Check for role matches or similar roles
        matched_roles = resume_roles_set.intersection(jd_roles_set)
        
        if matched_roles:
            return 100  # Perfect match
        
        # Check for partial matches (contains similar keywords)
        partial_matches = 0
        for resume_role in resume_roles_set:
            for jd_role in jd_roles_set:
                if any(word in resume_role for word in jd_role.split()) or \
                   any(word in jd_role for word in resume_role.split()):
                    partial_matches += 1
                    break
        
        if partial_matches > 0:
            return min(80, partial_matches * 30)  # Partial match score
        
        # If no role overlap but resume has relevant roles, give some points
        if resume_roles:
            return 30
        
        return 0
    
    def calculate_experience_score(self, resume_experience, jd_experience, resume_education, jd_education):
        """Calculate experience and education match score."""
        experience_score = 0
        education_score = 0
        
        # Experience scoring
        if jd_experience > 0:
            if resume_experience >= jd_experience:
                experience_score = 100
            elif resume_experience >= jd_experience * 0.7:  # Within 70% of required
                experience_score = 80
            elif resume_experience >= jd_experience * 0.5:  # Within 50% of required
                experience_score = 60
            else:
                experience_score = max(20, (resume_experience / jd_experience) * 40)
        else:
            experience_score = 70 if resume_experience > 0 else 50
        
        # Education scoring
        if jd_education > 0:
            if resume_education >= jd_education:
                education_score = 100
            elif resume_education >= jd_education - 1:  # One level below
                education_score = 70
            else:
                education_score = max(30, (resume_education / jd_education) * 50)
        else:
            education_score = 70 if resume_education > 0 else 50
        
        # Combine experience and education (equal weight)
        combined_score = (experience_score + education_score) / 2
        return combined_score
    
    def calculate_keyword_overlap_score(self, resume_keywords, jd_keywords):
        """Calculate keyword overlap score for additional context."""
        if not jd_keywords:
            return 0, [], []
        
        resume_keywords_set = set(keyword.lower() for keyword in resume_keywords[:20])  # Top 20
        jd_keywords_set = set(keyword.lower() for keyword in jd_keywords[:20])  # Top 20
        
        matched_keywords = list(resume_keywords_set.intersection(jd_keywords_set))
        missing_keywords = list(jd_keywords_set - resume_keywords_set)
        
        overlap_ratio = len(matched_keywords) / len(jd_keywords_set) if jd_keywords_set else 0
        keyword_score = overlap_ratio * 100
        
        return keyword_score, matched_keywords, missing_keywords
    
    def calculate_job_fit_score(self, resume_analysis, jd_analysis):
        """Calculate overall job fit score with detailed breakdown."""
        # Calculate individual scores
        skill_score, matched_skills, missing_skills = self.calculate_skill_overlap_score(
            resume_analysis['skills'], jd_analysis['skills']
        )
        
        role_score = self.calculate_role_relevance_score(
            resume_analysis['job_roles'], jd_analysis['job_roles']
        )
        
        experience_score = self.calculate_experience_score(
            resume_analysis['experience_years'], jd_analysis['experience_years'],
            resume_analysis['education_level'], jd_analysis['education_level']
        )
        
        # Calculate keyword overlap for additional insights
        keyword_score, matched_keywords, missing_keywords_general = self.calculate_keyword_overlap_score(
            resume_analysis['keywords'], jd_analysis['keywords']
        )
        
        # Combine matched keywords from skills and general keywords
        all_matched_keywords = list(set(matched_skills + matched_keywords))
        all_missing_keywords = list(set(missing_skills + missing_keywords_general))
        
        # Calculate weighted overall score
        overall_score = (
            skill_score * self.weights['skills'] +
            role_score * self.weights['role'] +
            experience_score * self.weights['experience']
        )
        
        # Round to nearest integer
        overall_score = round(overall_score)
        
        logging.debug(f"Score breakdown - Skills: {skill_score:.1f}, Role: {role_score:.1f}, "
                     f"Experience: {experience_score:.1f}, Overall: {overall_score}")
        
        return {
            'overall_score': overall_score,
            'skill_score': round(skill_score),
            'role_score': round(role_score),
            'experience_score': round(experience_score),
            'keyword_score': round(keyword_score),
            'matched_keywords': all_matched_keywords,
            'missing_keywords': all_missing_keywords,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills
        }
    
    def generate_suggestions(self, resume_analysis, jd_analysis, score_data):
        """Generate actionable improvement suggestions."""
        suggestions = []
        
        # Skill-based suggestions
        if score_data['skill_score'] < 70:
            missing_skills = score_data['missing_skills'][:5]  # Top 5 missing skills
            if missing_skills:
                suggestions.append({
                    'category': 'Skills',
                    'priority': 'High',
                    'suggestion': f"Add these key skills to your resume: {', '.join(missing_skills)}",
                    'description': 'These skills are specifically mentioned in the job description but missing from your resume.'
                })
        
        # Role relevance suggestions
        if score_data['role_score'] < 60:
            suggestions.append({
                'category': 'Role Alignment',
                'priority': 'High',
                'suggestion': 'Better align your job titles and role descriptions with the target position',
                'description': 'Use similar terminology and highlight relevant role responsibilities that match the job description.'
            })
        
        # Experience suggestions
        if score_data['experience_score'] < 70:
            jd_experience = jd_analysis['experience_years']
            resume_experience = resume_analysis['experience_years']
            
            if jd_experience > resume_experience:
                suggestions.append({
                    'category': 'Experience',
                    'priority': 'Medium',
                    'suggestion': f'Highlight relevant projects or internships to demonstrate {jd_experience}+ years equivalent experience',
                    'description': 'Include freelance work, personal projects, or volunteer experience that showcases relevant skills.'
                })
        
        # Keyword optimization suggestions
        if score_data['keyword_score'] < 50:
            missing_keywords = score_data['missing_keywords'][:3]  # Top 3 missing keywords
            if missing_keywords:
                suggestions.append({
                    'category': 'Keywords',
                    'priority': 'Medium',
                    'suggestion': f"Incorporate these keywords naturally: {', '.join(missing_keywords)}",
                    'description': 'These terms appear frequently in the job description and should be included in your resume.'
                })
        
        # Education suggestions
        if jd_analysis['education_level'] > resume_analysis['education_level']:
            suggestions.append({
                'category': 'Education',
                'priority': 'Low',
                'suggestion': 'Consider highlighting relevant certifications or continuing education',
                'description': 'If you lack the preferred degree level, emphasize professional certifications and training.'
            })
        
        # General optimization suggestions
        if score_data['overall_score'] < 80:
            suggestions.append({
                'category': 'General',
                'priority': 'Medium',
                'suggestion': 'Tailor your resume more specifically to this job description',
                'description': 'Use similar language and emphasize experiences that directly relate to the job requirements.'
            })
        
        # If score is very high, give positive reinforcement
        if score_data['overall_score'] >= 85:
            suggestions.append({
                'category': 'Excellent Match',
                'priority': 'Low',
                'suggestion': 'Your resume shows strong alignment with this position!',
                'description': 'Consider fine-tuning minor details and ensuring your cover letter reinforces key matching points.'
            })
        
        return suggestions
