from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import pickle
import sys

sys.path.append("../src")

from Corpus import Corpus

app = Flask(__name__, static_folder="../web", static_url_path="")

# Charger le corpus
df = pd.read_csv("../notebooks/discours_US.csv", sep="\t")
corpus = Corpus("discours_US")
for _, row in df.iterrows():
    corpus.add_document(
        titre=row["descr"],
        auteur=row["speaker"],
        date=row["date"],
        url=row["link"],
        texte=row["text"]
    )

with open("../notebooks/engine.pkl", "rb") as f:
    engine = pickle.load(f)

# ------------------ ROUTES HTML ------------------

@app.route("/")
def home():
    return send_from_directory("../web", "index.html")

@app.route("/filters")
def filters():
    authors = ["Tous"] + sorted(list(df["speaker"].unique()))
    dates = ["Toutes"] + sorted(list(df["date"].unique()))
    return jsonify({"authors": authors, "dates": dates})

# ------------------ API SEARCH ------------------

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

# ------------------ API EVOLUTION ------------------

@app.route("/evolution", methods=["POST"])
def evolution():
    data = request.json
    mot = data.get("mot", "").lower()

    freq = {}
    for doc_id, doc in corpus.id2doc.items():
        year = pd.to_datetime(doc.date, errors="coerce").year
        if year is None:
            continue

        count = doc.texte.lower().split().count(mot)
        freq[year] = freq.get(year, 0) + count

    out = [{"year": y, "freq": freq[y]} for y in sorted(freq.keys())]
    return jsonify(out)

# ------------------ STATIC FILES (LAST!!) ------------------

@app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory("../web", path)

# ------------------ RUN ------------------

if __name__ == "__main__":
    app.run(debug=True)
