from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
import os
from hieroglyph import get_hieroglyph

app = Flask(__name__)
CORS(app)

# Load trained model and label map
model = load_model("hieroglyph_model.h5")
labels = ["A1", "A2", "A3"]  # Adapte com seus códigos reais

def preprocess(img):
    img = img.resize((64, 64))  # Tamanho que o modelo foi treinado
    img = np.array(img) / 255.0
    return img.reshape((1, 64, 64, 3))

@app.route('/translate/<code>', methods=['GET'])
def translate(code):
    result = get_hieroglyph(code)
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Hieroglyph not found"}), 404

@app.route('/translate', methods=['POST'])
def translate_post():
    data = request.get_json()
    code = data.get('code')
    if not code:
        return jsonify({"error": "Code is required"}), 400
    result = get_hieroglyph(code)
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Hieroglyph not found"}), 404

@app.route('/translate/multi', methods=['POST'])
def translate_multi():
    data = request.get_json()
    code_string = data.get('code')
    if not code_string:
        return jsonify({"error": "Code is required"}), 400
    codes = code_string.split("-")
    results = []
    not_found = []
    for code in codes:
        result = get_hieroglyph(code)
        if result:
            results.append({
                "code": code,
                "transliteration": result["transliteration"],
                "meaning": result["meaning"]
            })
        else:
            not_found.append(code)
    return jsonify({
        "results": results,
        "not_found": not_found
    })

# Upload de imagem para identificar o hieróglifo
@app.route('/upload', methods=['POST'])
def upload_and_classify():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    file = request.files['image']
    
    try:
        img = Image.open(file.stream).convert("RGB")
        input_img = preprocess(img)
        prediction = model.predict(input_img)[0]
        idx = np.argmax(prediction)
        code = labels[idx]
        
        result = get_hieroglyph(code)
        if result:
            return jsonify({
                "code": code,
                "transliteration": result["transliteration"],
                "meaning": result["meaning"],
                "confidence": float(prediction[idx])
            })
        else:
            return jsonify({"error": "Hieroglyph not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


