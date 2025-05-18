import os
import whisper
from Utils.publisher import publish_message
import torch
from Services.answer_match_engine import answer_match
import json

device = "cuda" if torch.cuda.is_available() else "cpu"
# Load the model on the selected device
model = whisper.load_model("tiny.en", device=device)

def transcribe_audio(audio_path, metadata):
    """
    Transcribe audio using the Whisper model on the specified device (GPU or CPU).
    The transcription result is printed to the console.
    """
    try:
        pid = os.getpid()  # Get the process ID
        print(f"\n--Process {pid} is starting to process file: {audio_path}")

        # Perform transcription
        print(f"\n[*]Transcribing audio: {audio_path}\n")
        result = model.transcribe(audio_path, fp16=(device == "cuda"))
        print(f'\nTranscribed text: {result["text"]}\n')
        print(f'\n\n--- metadata:: {metadata}\n\n')
        if result['text']:
            try:
                report = answer_match(
                    metadata['question_id'], result['text'])
            except Exception as e:
                print(f"Error in answer matching: {str(e)}")

            data_to_send = {"id": metadata["question_id"], "question": metadata["question"], "transcribed_text": result["text"],
                            "token": metadata["token"], "loggedInEmail": metadata["loggedInEmail"], "session_id": metadata["session_id"], "report": report}
            print(f'\n------ data_to_send:: {data_to_send} ----\n')
            try:
                publish_message("transcribed-text", json.dumps(data_to_send))
            except Exception as e:
                print(f"Error publishing message: {str(e)}")
        else:
            print("f\nTranscribed text is empty")
    except Exception as e:
        print(f"Error during transcription of {audio_path}: {str(e)}")
    finally:
        if os.path.exists(audio_path):
            try:
                os.remove(audio_path)
                print(f"File {audio_path} removed successfully.")
            except Exception as e:
                print(f"Error removing file {audio_path}: {str(e)}")