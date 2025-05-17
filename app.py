from flask import Flask, request, jsonify
from db import get_meaning_by_code

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"mensagem": "API Tradutora de Hieróglifos (com PostgreSQL remoto)"})

@app.route("/traduzir/mdc", methods=["GET"])
def traduzir():
    mdc = request.args.get("codigo")
    if not mdc:
        return jsonify({"erro": "Parâmetro 'codigo' é obrigatório"}), 400

    partes = mdc.split("-")
    traducoes = []

    for parte in partes:
        resultado = get_meaning_by_code(parte.strip())
        if resultado:
            traducoes.append(resultado["meaning"])
        else:
            traducoes.append(f"[{parte.strip()}]")

    return jsonify({
        "entrada": mdc,
        "traducao": " ".join(traducoes),
        "palavras": traducoes
    })

if __name__ == "__main__":
    app.run(debug=True)
