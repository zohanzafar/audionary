from gtts import gTTS
import uuid
from django.conf import settings
import os

def generate_audio(text, filename=None):
    filename = filename or f"{uuid.uuid4().hex}.mp3"
    path = os.path.join(settings.MEDIA_ROOT, 'audio', filename)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    tts = gTTS(text=text)
    tts.save(path)
    return filename
