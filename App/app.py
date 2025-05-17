from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
from db import get_hieroglyph

app = Flask(__name__)
CORS(app)

model = load_model("hieroglyph_model.h5")

labels = []  

def preprocess(img):
    img = img.resize((64, 64))
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
                "description": result["description"],
                "ideogram": result["ideogram"],
                'symbol': result["symbol"]
            })
        else:
            not_found.append(code)
    return jsonify({
        "results": results,
        "not_found": not_found
    })

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
        
        if idx >= len(labels):
            return jsonify({"error": "Label index out of range"}), 500
        
        code = labels[idx]
        result = get_hieroglyph(code)
        if result:
            return jsonify({
                "code": code,
                "description": result["description"],
                "symbol": result["symbol"],
                "ideogram": result["ideogram"],
                "confidence": float(prediction[idx]),
                "images": result["images"]
            })
        else:
            return jsonify({"error": "Hieroglyph not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
