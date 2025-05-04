from flask import Flask, request, send_file
from gtts import gTTS
import tempfile
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "Servidor COMET activo"

@app.route('/audio', methods=['POST'])
def audio():
    if 'Content-Type' not in request.headers or request.headers['Content-Type'] != 'audio/wav':
        return "Tipo de contenido no soportado", 400

    # Guardar archivo temporalmente
    audio_path = tempfile.mktemp(suffix=".wav")
    with open(audio_path, 'wb') as f:
        f.write(request.data)

    print(f"✅ Audio recibido: {audio_path}")

    # Generar respuesta con gTTS (puedes cambiar el texto según el análisis)
    texto = "Hola, estoy aquí para escucharte. Todo estará bien."
    tts = gTTS(text=texto, lang='es')
    respuesta_path = tempfile.mktemp(suffix=".mp3")
    tts.save(respuesta_path)

    return send_file(respuesta_path, mimetype="audio/mpeg")
