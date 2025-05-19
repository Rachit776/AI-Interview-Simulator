import os
import traceback
from flask import request, jsonify
from multiprocessing import Process
from config import UPLOAD_FOLDER
from Utils.convert_to_wav import convert_to_wav
from Services.Transcribe_audio import transcribe_audio
from Utils.generate_filename import generate_timestamp_based_filename

# Allowed audio file extensions
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a', 'aac'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if not file or file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file type"}), 400

    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Generate a unique filename
    unique_filename = generate_timestamp_based_filename(file.filename)
    original_file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

    try:
        # Save original file
        file.save(original_file_path)

        # Convert to WAV format if needed
        wav_file_path = convert_to_wav(original_file_path)

        # Delete original file if different from WAV
        if wav_file_path != original_file_path and os.path.exists(original_file_path):
            os.remove(original_file_path)

        # Metadata from form
        metadata = {
            "file_name": file.filename,
            "unique_filename": unique_filename,
            "question_id": request.form.get("id"),
            "question": request.form.get("question"),
            "token": request.form.get("token"),
            "loggedInEmail": request.form.get("loggedInEmail"),
            "session_id": request.form.get("session_id")
        }

        # Start background transcription
        process = Process(target=transcribe_audio, args=(wav_file_path, metadata))
        process.daemon = True
        process.start()

        # Response
        return jsonify({
            "message": "Audio uploaded and transcription started.",
            "file_url": f"/uploads/{os.path.basename(wav_file_path)}"
        }), 200

    except Exception as e:
        # Print full traceback for Render logs
        print("[ERROR] Upload failed:")
        traceback.print_exc()
        return jsonify({"error": "Failed to process audio file"}), 500
