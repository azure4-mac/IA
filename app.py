from flask import Flask, request, jsonify
from hieroglyph import get_hieroglyph
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
