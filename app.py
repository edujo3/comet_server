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
    # Verifica encabezado correcto
    if request.content_type != 'audio/wav':
        return "Tipo de contenido no soportado", 400

    # Guarda el audio en un archivo temporal
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_audio.write(request.data)
    temp_audio.close()
    print(f"✅ Archivo de audio recibido y guardado en: {temp_audio.name}")

    # Procesar con gTTS
    texto = "Hola, te escucho. ¿Cómo te sientes hoy?"
    tts = gTTS(text=texto, lang='es')
    respuesta_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    tts.save(respuesta_path)

    print(f"🔊 Enviando archivo de respuesta: {respuesta_path}")
    return send_file(respuesta_path, mimetype="audio/mpeg")
