import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from Services.recommemendation_engine import recommend_questions
from Services.upload_audio import upload_audio
from Utils import download_nltk_data
from config import UPLOAD_FOLDER

# Initialize Flask app
app = Flask(__name__)

# Set upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Enable CORS
CORS(app)

# Optional: Download NLTK data
download_nltk_data.download()

# Enable CORS headers manually
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

# Health check route
@app.route("/")
def index():
    return "Working"

# Static file serving route for uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Register routes
app.add_url_rule('/recommend-questions', 'recommend_questions', recommend_questions, methods=['POST'])
app.add_url_rule('/upload', 'upload_audio', upload_audio, methods=['POST'])

# Start the Flask app (for local dev; Render uses gunicorn)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True, threaded=True)
