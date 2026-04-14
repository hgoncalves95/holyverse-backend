from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import random
import requests

app = Flask(__name__)
CORS(app)

with open("versiculos.json", "r", encoding="utf-8") as f:
    versiculos = json.load(f)

def detectar_sentimento(texto):
    texto = texto.lower()

    sentimentos = {
        "tristeza": ["triste", "desanimado", "deprimido", "pra baixo", "sozinho", "mal"],
        "ansiedade": ["ansioso", "preocupado", "nervoso", "aflito", "angustiado"],
        "medo": ["medo", "inseguro", "assustado", "receio"],
        "gratidao": ["grato", "agradecido", "abençoado"],
        "cansaco": ["cansado", "exausto", "sem energia", "esgotado"],
        "alegria": ["feliz", "alegre", "animado", "contente"]
    }

    pontuacao = {s: 0 for s in sentimentos}

    for sentimento, palavras in sentimentos.items():
        for palavra in palavras:
            if palavra in texto:
                pontuacao[sentimento] += 1

    melhor = max(pontuacao, key=pontuacao.get)

    if pontuacao[melhor] == 0:
        return None

    return melhor

mapa = {
    "tristeza": "psalms",
    "ansiedade": "peace",
    "medo": "fear",
    "gratidao": "praise",
    "cansaco": "rest",
    "alegria": "joy"
}

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

@app.route("/versiculo/<sentimento>")
def get_versiculo(sentimento):
    sentimento = sentimento.lower()

    verso = buscar_api(sentimento)

    if not verso:
        if sentimento not in versiculos:
            return jsonify({"erro": "Sentimento não encontrado"}), 404

        verso = random.choice(versiculos[sentimento])

    return jsonify({"versiculo": verso})

@app.route("/analisar", methods=["POST"])
def analisar():
    dados = request.json
    texto = dados.get("texto", "")

    sentimento = detectar_sentimento(texto)

    if not sentimento:
        return jsonify({
            "erro": "Não consegui entender como você está se sentindo. Tente algo como: 'estou triste' ou 'estou ansioso'."
        })

    verso = buscar_api(sentimento)

    if not verso:
        verso = random.choice(versiculos[sentimento])

    return jsonify({
        "sentimento": sentimento,
        "versiculo": verso
    })

if __name__ == "__main__":
    app.run(debug=True)
