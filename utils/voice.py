import tempfile
from pydub import AudioSegment
import speech_recognition as sr
import os

def convert_to_wav(input_path: str) -> str:
    out_wav = tempfile.mktemp(suffix=".wav")
    audio = AudioSegment.from_file(input_path)
    audio.export(out_wav, format="wav")
    return out_wav

def voice_to_text(file_path: str, languages=("uz-UZ","en-US","ru-RU")) -> str:
    r = sr.Recognizer()
    try:
        wav = convert_to_wav(file_path)
    except Exception:
        return ""
    with sr.AudioFile(wav) as source:
        audio_data = r.record(source)
    for lang in languages:
        try:
            text = r.recognize_google(audio_data, language=lang)
            os.remove(wav)
            return text
        except Exception:
            continue
    try:
        os.remove(wav)
    except Exception:
        pass
    return ""
