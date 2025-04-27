from flask import Flask, request, jsonify
import io
from PIL import Image
import base64
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ COMET Server funcionando correctamente"

@app.route("/analyze", methods=["POST"])
def analyze():
    # Verificar si hay un archivo en la solicitud
    if 'image' not in request.files:
        return jsonify({"error": "No se encontró ninguna imagen en la solicitud."}), 400

    # Leer la imagen enviada
    image_file = request.files['image']
    image_bytes = image_file.read()

    # (Opcional) Procesar la imagen aquí (por ahora solo simular)
    # Podrías usar IA para análisis real.

    # Para ahora: detectar rostro "simulado" (en el futuro usar OpenAI Vision si quieres)
    face_detected = True
    emotion = "happy"  # Podrías cambiarlo luego dinámicamente.

    # Devolver respuesta JSON
    return jsonify({
        "face_detected": face_detected,
        "emotion": emotion
    })

# Nota: No coloques if __name__ == "__main__" porque Gunicorn levantará la app automáticamente
