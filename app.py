from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app)

with open("versiculos.json", "r", encoding="utf-8") as f:
    versiculos = json.load(f)

# 🔥 IA SIMPLES (detecção de sentimento)
def detectar_sentimento(texto):
    texto = texto.lower()

    if any(p in texto for p in ["cansado", "exausto", "sem energia"]):
        return "cansaco"
    elif any(p in texto for p in ["triste", "desanimado", "deprimido"]):
        return "tristeza"
    elif any(p in texto for p in ["ansioso", "preocupado", "nervoso"]):
        return "ansiedade"
    elif any(p in texto for p in ["medo", "inseguro"]):
        return "medo"
    elif any(p in texto for p in ["grato", "agradecido"]):
        return "gratidao"
    else:
        return "alegria"

# 🔹 rota antiga (botões)
@app.route("/versiculo/<sentimento>")
def get_versiculo(sentimento):
    sentimento = sentimento.lower()

    if sentimento not in versiculos:
        return jsonify({"erro": "Sentimento não encontrado"}), 404

    verso = random.choice(versiculos[sentimento])
    return jsonify({"versiculo": verso})

# 🔥 rota IA (novo)
@app.route("/analisar", methods=["POST"])
def analisar():
    dados = request.json
    texto = dados.get("texto", "")

    sentimento = detectar_sentimento(texto)
    verso = random.choice(versiculos[sentimento])

    return jsonify({
        "sentimento": sentimento,
        "versiculo": verso
    })

if __name__ == "__main__":
    app.run(debug=True)