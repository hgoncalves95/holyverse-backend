from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import random
import requests

app = Flask(__name__)
CORS(app)

with open("versiculos.json", "r", encoding="utf-8") as f:
    versiculos = json.load(f)

# 🔥 detectar sentimento
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

# 🔥 mapa sentimento → busca
mapa = {
    "tristeza": "psalms",
    "ansiedade": "peace",
    "medo": "fear",
    "gratidao": "praise",
    "cansaco": "rest",
    "alegria": "joy"
}

# 🔥 buscar da API
def buscar_api(sentimento):
    try:
        tema = mapa.get(sentimento, "faith")
        url = f"https://bible-api.com/{tema}"

        res = requests.get(url, timeout=3)
        data = res.json()

        if "text" in data:
            return data["text"].strip()

    except:
        return None

# 🔹 rota botão
@app.route("/versiculo/<sentimento>")
def get_versiculo(sentimento):
    sentimento = sentimento.lower()

    # tenta API primeiro
    verso = buscar_api(sentimento)

    # fallback pro JSON
    if not verso:
        if sentimento not in versiculos:
            return jsonify({"erro": "Sentimento não encontrado"}), 404

        verso = random.choice(versiculos[sentimento])

    return jsonify({"versiculo": verso})

# 🔥 rota IA
@app.route("/analisar", methods=["POST"])
def analisar():
    dados = request.json
    texto = dados.get("texto", "")

    sentimento = detectar_sentimento(texto)

    # tenta API
    verso = buscar_api(sentimento)

    # fallback JSON
    if not verso:
        verso = random.choice(versiculos[sentimento])

    return jsonify({
        "sentimento": sentimento,
        "versiculo": verso
    })

if __name__ == "__main__":
    app.run(debug=True)
