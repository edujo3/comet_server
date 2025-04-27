from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = '/tmp'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return '✅ COMET Server funcionando correctamente'

@app.route('/receive_image', methods=['POST'])
def receive_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No se encontró el campo "image".'}), 400

        image = request.files['image']

        if image.filename == '':
            return jsonify({'error': 'Nombre de archivo vacío.'}), 400

        # Solo continuar si el archivo es imagen
        if not image.mimetype.startswith('image/'):
            return jsonify({'error': 'El archivo no es una imagen válida.'}), 400

        # Guardar archivo en /tmp
        filename = f"captura_{int(time.time())}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        image.save(filepath)

        print(f"✅ Imagen recibida: {filepath}")

        return jsonify({'message': 'Imagen recibida exitosamente.'}), 200

    except Exception as e:
        print(f"❌ Error en servidor: {e}")
        return jsonify({'error': 'Error procesando la imagen.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
