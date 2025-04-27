from flask import Flask, request, jsonify
from PIL import Image
import io

app = Flask(__name__)

# Limitar el tamaño máximo de subida (ejemplo: 5MB)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB

@app.route('/')
def home():
    return "✅ COMET Server funcionando correctamente"

@app.route('/receive_image', methods=['POST'])
def receive_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file in the request"}), 400

        file = request.files['image']

        if not file:
            return jsonify({"error": "No file received"}), 400

        image_bytes = file.read()

        # Verificar que se leyó algo
        if not image_bytes:
            return jsonify({"error": "Empty image file"}), 400

        # Abrir la imagen para validar que es imagen
        image = Image.open(io.BytesIO(image_bytes))
        print(f"✅ Imagen recibida: {image.format}, tamaño: {image.size}")

        return jsonify({"message": "Image received successfully!"})

    except Exception as e:
        print(f"🚨 Error procesando imagen: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
