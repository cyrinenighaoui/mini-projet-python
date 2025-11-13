from datetime import datetime
from Author import Author
from document import document
import pandas as pd

class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}     # name → Author
        self.id2doc = {}      # id → Document
        self.ndoc = 0
        self.naut = 0

    def add_document(self, titre, auteur, date, url, texte):
        doc = document(titre, auteur, date, url, texte)
        doc_id = f"doc_{self.ndoc}"
        self.id2doc[doc_id] = doc
        self.ndoc += 1

        author_list = [a.strip() for a in auteur.split(",")]

        for name in author_list:
            if name not in self.authors:
                self.authors[name] = Author(name)
                self.naut += 1

            self.authors[name].add(doc_id, doc)

    def afficher_par_date(self, n):
        docs_sorted = sorted(
            self.id2doc.values(),
            key=lambda doc: datetime.strptime(doc.date, "%Y-%m-%d")
        )
        for doc in docs_sorted[:n]:
            doc.afficher()
            print()

    def afficher_par_titre(self, n):
        docs_sorted = sorted(
            self.id2doc.values(),
            key=lambda doc: doc.titre.lower()
        )
        for doc in docs_sorted[:n]:
            doc.afficher()
            print()

    def __repr__(self):
        return f"<Corpus {self.nom}: {self.ndoc} documents, {self.naut} auteurs>"

    # ──────────────────────────────────────────────────
    #  SAUVEGARDE CSV
    # ──────────────────────────────────────────────────
    def save(self, filename):
        data = []

        for doc_id, doc in self.id2doc.items():
            data.append({
                "id": doc_id,
                "titre": doc.titre,
                "auteur": doc.auteur,
                "date": doc.date,
                "url": doc.url,
                "texte": doc.texte
            })

        df = pd.DataFrame(data)
        df.to_csv(filename, sep="\t", index=False)
        print(f"Corpus sauvegardé dans {filename}")

    # ──────────────────────────────────────────────────
    #   CHARGEMENT CSV
    # ──────────────────────────────────────────────────
    def load(self, filename):
        df = pd.read_csv(filename, sep="\t")

        # Reset si on recharge
        self.id2doc = {}
        self.authors = {}
        self.ndoc = 0
        self.naut = 0

        for _, row in df.iterrows():
            self.add_document(
                titre=row["titre"],
                auteur=row["auteur"],
                date=row["date"],
                url=row["url"],
                texte=row["texte"]
            )

        print(f"Corpus chargé depuis {filename} ({len(df)} documents)")
