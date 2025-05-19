from pydub import AudioSegment
import os
import mimetypes
import traceback

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def convert_to_wav(audio_path):
    """
    Convert the audio file to WAV format using pydub.
    Returns the path to the WAV file.
    """
    try:
        # Guess format based on MIME type or fallback to file extension
        mime_type, _ = mimetypes.guess_type(audio_path)
        format_ext = mime_type.split('/')[-1] if mime_type else os.path.splitext(audio_path)[1][1:]

        # Load and convert
        audio = AudioSegment.from_file(audio_path, format=format_ext)
        wav_path = os.path.splitext(audio_path)[0] + ".wav"
        audio.export(wav_path, format="wav")

        return wav_path

    except Exception as e:
        print(f"[ERROR] Failed to convert {audio_path} to WAV:")
        traceback.print_exc()
        raise e  # Propagate to caller (upload handler will catch it)
