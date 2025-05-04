from flask import Flask, request, send_file, jsonify
from gtts import gTTS
import openai
import tempfile
import os

app = Flask(__name__)

# Asegúrate de tener esta variable en Render o un archivo .env
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "Servidor COMET operativo ✅"

@app.route("/audio", methods=["POST"])
def procesar_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No se encontró el archivo de audio"}), 400

    audio_file = request.files['audio']

    # Guardar temporalmente el audio
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
        audio_path = tmp_wav.name
        audio_file.save(audio_path)

    try:
        # 1. Transcripción con Whisper
        with open(audio_path, "rb") as f:
            transcript = openai.Audio.transcribe("whisper-1", f)

        texto = transcript["text"]
        print(f"📝 Transcripción: {texto}")

        # 2. ChatGPT
        chat_response = openai.ChatCompletion.create(
            model="gpt-4",  # Cambia a "gpt-3.5-turbo" si no tienes acceso a GPT-4
            messages=[
                {"role": "system", "content": "Eres un asistente emocional llamado COMET."},
                {"role": "user", "content": texto}
            ]
        )

        respuesta = chat_response["choices"][0]["message"]["content"]
        print(f"🤖 Respuesta ChatGPT: {respuesta}")

        # 3. Convertir texto a voz con gTTS
        tts = gTTS(respuesta, lang='es')
        temp_mp3 = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        tts.save(temp_mp3.name)

        # 4. Enviar archivo MP3 al ESP32
        return send_file(temp_mp3.name, mimetype="audio/mpeg")

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(audio_path)

# Para correr localmente (opcional)
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=10000)
