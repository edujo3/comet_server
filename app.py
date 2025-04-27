from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
import os

app = Flask(__name__)
CORS(app)

# 🔥 Aumentar el límite permitido de carga (por defecto en Flask es 16MB, pero aseguramos)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB

@app.route('/', methods=['GET'])
def index():
    return "✅ COMET Server funcionando correctamente"

@app.route('/receive_image', methods=['POST'])
def receive_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']

    try:
        img = Image.open(image_file.stream)
        width, height = img.size
        print(f"📷 Imagen recibida. Tamaño: {width}x{height}")
        return jsonify({'message': 'Imagen recibida correctamente', 'width': width, 'height': height}), 200
    except Exception as e:
        print("❌ Error procesando la imagen:", str(e))
        return jsonify({'error': 'Failed to process image'}), 500
