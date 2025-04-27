from flask import Flask, request, jsonify
from PIL import Image
import io

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return '✅ COMET Server funcionando correctamente'

@app.route('/receive_image', methods=['POST'])
def receive_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No se encontró archivo llamado "image"'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'}), 400

    try:
        # Leemos el archivo en memoria
        img = Image.open(file.stream)
        width, height = img.size
        print(f"✅ Imagen recibida: {file.filename}, tamaño: {width}x{height}")

        return jsonify({'message': f'Imagen recibida correctamente. Tamaño: {width}x{height}'})
    except Exception as e:
        print(f"❌ Error al procesar imagen: {str(e)}")
        return jsonify({'error': 'Error al procesar la imagen'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
