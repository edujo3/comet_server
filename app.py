from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return "✅ COMET Server funcionando correctamente", 200

@app.route('/receive_image', methods=['POST'])
def receive_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No se envió imagen'}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'}), 400

    # Guarda temporalmente la imagen
    save_path = os.path.join("/tmp", image.filename)
    image.save(save_path)

    print(f"✅ Imagen recibida y guardada: {save_path}")

    return jsonify({'message': 'Imagen recibida correctamente ✅'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
