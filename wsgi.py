import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

from app import create_app

app = create_app()

if __name__ == '__main__':
    # Running locally for dev purposes (in prod, a WSGI server should bind to this app instance)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
