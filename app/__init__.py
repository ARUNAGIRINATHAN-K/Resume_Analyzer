import os
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from app.config import Config

def create_app(config_class=Config):
    """Application factory for standard Flask app initialization."""
    app_dir = os.path.dirname(os.path.abspath(__file__))
    app = Flask(__name__,
                template_folder=os.path.join(app_dir, 'templates'),
                static_folder=os.path.join(app_dir, 'static'))
    app.config.from_object(config_class)
    
    # Apply ProxyFix to support running behind reverse proxies in production
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register routes blueprint
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app
