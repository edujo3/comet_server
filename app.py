from flask import Flask, request, send_file
import openai
from gtts import gTTS
import tempfile

app = Flask(__name__)
openai.api_key = 'TU_API_KEY_DE_OPENAI'

@app.route('/audio', methods=['POST'])
def procesar_audio():
    if 'audio' not in request.files:
        return 'No se encontró el archivo de audio', 400

    archivo_audio = request.files['audio']
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
        archivo_audio.save(temp_audio.name)

        # Transcribir el audio con Whisper
        transcripcion = openai.Audio.transcribe("whisper-1", open(temp_audio.name, "rb"))

        # Generar respuesta con ChatGPT
        respuesta_chat = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": transcripcion["text"]}]
        )

        respuesta_texto = respuesta_chat["choices"][0]["message"]["content"]

        # Convertir la respuesta en audio
        tts = gTTS(respuesta_texto, lang='es')
        archivo_respuesta = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
        tts.save(archivo_respuesta.name)

    return send_file(archivo_respuesta.name, mimetype='audio/mpeg')
