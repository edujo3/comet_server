from flask import Flask, request, jsonify
import requests
import base64
import os

app = Flask(__name__)

# Tu API Key de OpenAI (se carga de variables de entorno)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    image_bytes = file.read()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Detecta si hay un rostro humano en la imagen y cuál es su emoción (feliz, triste, neutro, enojado). Devuelve respuesta JSON {\"face_detected\": true/false, \"emotion\": \"feliz/triste/neutro/enojado\"}."},
                    {
                        "type": "image",
                        "image": base64_image
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        data = response.json()
        try:
            message = data['choices'][0]['message']['content']
            return message, 200
        except Exception as e:
            return jsonify({"error": "Parsing response error"}), 500
    else:
        return jsonify({"error": f"OpenAI API error {response.status_code}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
