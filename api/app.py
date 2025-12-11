from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import pickle
import os
import sys

# ---------------------------
# Fixer la racine du projet
# ---------------------------
BASE_DIR = "/app"   # IMPORTANT : fonctionne dans Docker

# Ajouter src au PYTHONPATH
sys.path.append(os.path.join(BASE_DIR, "src"))

from Corpus import Corpus

# ---------------------------
# Initialiser Flask
# ---------------------------
app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "web"),
    static_url_path="/static"
)

# ---------------------------
# Charger les données
# ---------------------------
DATA_PATH = os.path.join(BASE_DIR, "notebooks", "discours_US.csv")
ENGINE_PATH = os.path.join(BASE_DIR, "notebooks", "engine.pkl")

df = pd.read_csv(DATA_PATH, sep="\t")

corpus = Corpus("discours_US")
for _, row in df.iterrows():
    corpus.add_document(
        titre=row["descr"],
        auteur=row["speaker"],
        date=row["date"],
        url=row["link"],
        texte=row["text"]
    )

with open(ENGINE_PATH, "rb") as f:
    engine = pickle.load(f)

# ---------------------------
# ROUTES HTML
# ---------------------------

@app.route("/")
def home():
    return send_from_directory(os.path.join(BASE_DIR, "web"), "index.html")

@app.route("/static/<path:path>")
def static_files(path):
    return send_from_directory(os.path.join(BASE_DIR, "web"), path)

@app.route("/filters")
def filters():
    authors = ["Tous"] + sorted(list(df["speaker"].unique()))
    dates = ["Toutes"] + sorted(list(df["date"].unique()))
    return jsonify({"authors": authors, "dates": dates})

# ---------------------------
# API : SEARCH
# ---------------------------

@app.route("/search", methods=["POST"])
def search():
    data = request.json
    query = data.get("query", "")
    k = int(data.get("k", 5))
    author = data.get("author", "Tous")
    date = data.get("date", "Toutes")

    results = engine.search(query, top=9999)

    if author != "Tous":
        results = results[results["id"].apply(
            lambda doc_id: corpus.id2doc[doc_id].auteur == author
        )]

    if date != "Toutes":
        results = results[results["id"].apply(
            lambda doc_id: corpus.id2doc[doc_id].date == date
        )]

    return jsonify(results.head(k).to_dict(orient="records"))

# ---------------------------
# API : EVOLUTION
# ---------------------------

@app.route("/evolution", methods=["POST"])
def evolution():
    data = request.get_json(force=True)
    mot = data.get("mot", "").lower().strip()

    freq = {}

    for doc_id, doc in corpus.id2doc.items():
        # convertir proprement la date en année
        year = pd.to_datetime(doc.date, errors="coerce").year
        if pd.isna(year):
            continue  # si date pourrie, on saute

        year = int(year)

        # compter le mot dans le texte
        tokens = doc.texte.lower().split()
        count = tokens.count(mot)

        if count > 0:
            freq[year] = freq.get(year, 0) + count

    # transformer en liste triée pour le JSON
    out = [{"year": y, "freq": freq[y]} for y in sorted(freq.keys())]
    return jsonify(out)

# ---------------------------
# FLASK RUN
# ---------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
