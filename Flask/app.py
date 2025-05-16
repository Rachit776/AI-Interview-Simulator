from flask import Flask
from flask_cors import CORS
from Services.recommemendation_engine import recommend_questions
from Services.upload_audio import upload_audio

app = Flask(__name__)
CORS(app)  # Allow all origins by default

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

# Register routes
app.add_url_rule('/recommend-questions', 'recommend_questions', recommend_questions, methods=['POST'])
app.add_url_rule('/upload', 'upload_audio', upload_audio, methods=['POST'])

@app.route("/")
def index():
    return "Working"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True,threaded=True)
