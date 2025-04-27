from flask import Flask, request, jsonify
from PIL import Image
import io

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return '✅ COMET Server funcionando correctamente'

@app.route('/receive_image', methods=['POST'])
def receive_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No se encontró archivo llamado "image"'}), 400

        image_file = request.files['image']

        # Leer la imagen con PIL
        img = Image.open(image_file.stream)

        width, height = img.size
        print(f"📸 Imagen recibida correctamente: {width}x{height}")

        return jsonify({'message': f'Imagen recibida correctamente. Tamaño: {width}x{height}'})

    except Exception as e:
        print(f"❌ Error procesando la imagen: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
