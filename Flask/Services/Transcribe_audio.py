import os
import whisper
from Utils.publisher import publish_message
import torch
from Services.answer_match_engine import answer_match
import json
import traceback

device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("tiny.en", device=device)

def transcribe_audio(audio_path, metadata):
    """
    Transcribe audio using Whisper model on the specified device (GPU or CPU).
    Sends transcription and answer match report via a message publisher.
    Cleans up the audio file after processing.
    """
    pid = os.getpid()
    print(f"\n-- Process {pid} starting transcription for file: {audio_path}")

    try:
        print(f"[*] Transcribing audio: {audio_path}")
        result = model.transcribe(audio_path, fp16=(device == "cuda"))
        transcribed_text = result.get("text", "").strip()
        print(f"[+] Transcribed text: {transcribed_text}")

        if not transcribed_text:
            print("[!] Transcribed text is empty. Skipping further processing.")
            return

        # Generate answer match report
        try:
            report = answer_match(metadata.get('question_id'), transcribed_text)
        except Exception as e:
            print(f"[ERROR] answer_match failed: {str(e)}")
            traceback.print_exc()
            report = None

        data_to_send = {
            "id": metadata.get("question_id"),
            "question": metadata.get("question"),
            "transcribed_text": transcribed_text,
            "token": metadata.get("token"),
            "loggedInEmail": metadata.get("loggedInEmail"),
            "session_id": metadata.get("session_id"),
            "report": report
        }

        print(f"[DEBUG] Data to publish: {data_to_send}")

        try:
            publish_message("transcribed-text", json.dumps(data_to_send))
            print("[+] Published transcribed text message successfully.")
        except Exception as e:
            print(f"[ERROR] Publishing message failed: {str(e)}")
            traceback.print_exc()

    except Exception as e:
        print(f"[ERROR] Transcription failed for {audio_path}: {str(e)}")
        traceback.print_exc()

    finally:
        # Clean up audio file
        if os.path.exists(audio_path):
            try:
                os.remove(audio_path)
                print(f"[INFO] Removed file: {audio_path}")
            except Exception as e:
                print(f"[ERROR] Failed to remove file {audio_path}: {str(e)}")
