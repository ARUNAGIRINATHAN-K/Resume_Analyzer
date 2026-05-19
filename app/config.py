import os

class Config:
    """Standard application configuration for production."""
    SECRET_KEY = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
    
    # Paths relative to the app directory
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    
    # Limits
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
    ALLOWED_EXTENSIONS = {'pdf'}
