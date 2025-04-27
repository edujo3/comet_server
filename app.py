from flask import Flask, request, jsonify
from PIL import Image
import io

app = Flask(__name__)

# Limitar el tamaño máximo de subida (ejemplo: 5MB)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB

@app.route('/')
def home():
    return jsonify({"message": "Hello from COMET Server!"})

@app.route('/receive_image', methods=['POST'])
def receive_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Leer la imagen recibida
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        print(f"Imagen recibida: {image.format}, {image.size}, {image.mode}")

        return jsonify({"message": "Image received successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
