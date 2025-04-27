from flask import Flask, request, jsonify
from PIL import Image
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return "✅ COMET Server funcionando correctamente"

@app.route('/receive_image', methods=['POST'])
def receive_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No se recibió ningún archivo llamado "image"'}), 400

        image_file = request.files['image']
        
        if image_file.filename == '':
            return jsonify({'error': 'Nombre de archivo vacío'}), 400

        # Leer imagen en memoria
        img_bytes = image_file.read()
        img = Image.open(io.BytesIO(img_bytes))
        
        # Convertir la imagen a Base64 para visualizar si queremos
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        print("✅ Imagen recibida y procesada exitosamente. Tamaño:", img.size)

        return jsonify({'message': 'Imagen recibida correctamente', 'width': img.width, 'height': img.height})

    except Exception as e:
        print("⚠️ Error procesando la imagen:", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
