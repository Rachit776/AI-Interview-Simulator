import os
from flask import Flask, send_from_directory, request, make_response
from flask_cors import CORS
from Services.recommemendation_engine import recommend_questions
from Services.upload_audio import upload_audio
from Utils import download_nltk_data
from config import UPLOAD_FOLDER

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Enable CORS (let flask_cors handle OPTIONS automatically)
CORS(app, resources={r"/*": {"origins": "*"}})

# Optional: Download NLTK data on startup
download_nltk_data.download()

# Health check route
@app.route("/")
def index():
    return "Working"

# Static file serving route for uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Wrapper to handle OPTIONS requests for recommend_questions
@app.route('/recommend-questions', methods=['POST', 'OPTIONS'])
def recommend_questions_route():
    if request.method == 'OPTIONS':
        # Preflight response
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response
    return recommend_questions()

# Wrapper to handle OPTIONS requests for upload_audio
@app.route('/upload', methods=['POST', 'OPTIONS'])
def upload_audio_route():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response
    return upload_audio()

# Run locally (Render will use gunicorn)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True, threaded=True)
