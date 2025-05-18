import os
from flask import Flask
from flask_cors import CORS
from Services.recommemendation_engine import recommend_questions
from Services.upload_audio import upload_audio
from Utils import download_nltk_data

# Initialize Flask app
app = Flask(__name__)

# Allow Cross-Origin Resource Sharing
CORS(app)

# Optional: Download NLTK data on startup (make sure it’s lightweight and idempotent)
download_nltk_data.download()

# Set upload folder from environment or default
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', './uploads')

# Enable CORS headers manually for all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

# Register routes
app.add_url_rule('/recommend-questions', 'recommend_questions', recommend_questions, methods=['POST'])
app.add_url_rule('/upload', 'upload_audio', upload_audio, methods=['POST'])

# Health check route
@app.route("/")
def index():
    return "Working"

# Start the Flask app (for local development only)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT env var automatically
    app.run(host="0.0.0.0", port=port, debug=True, threaded=True)
