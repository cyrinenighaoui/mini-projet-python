from datetime import datetime
import pandas as pd
from Author import Author
from document import Document
import re

class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

    def add_document(self, titre, auteur, date, url, texte):
        doc = Document(titre, auteur, date, url, texte)
        doc_id = f"doc_{self.ndoc}"
        self.id2doc[doc_id] = doc
        self.ndoc += 1
        author_str = str(auteur) if auteur is not None else "Unknown"
        author_list = [a.strip() for a in author_str.split(",")]


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

    def save(self, filename):
        data = []

        for doc_id, doc in self.id2doc.items():
            data.append({
                "id": doc_id,
                "titre": doc.titre,
                "auteur": doc.auteur,
                "date": doc.date,
                "url": doc.url,
                "texte": doc.texte,
                "type": doc.getType()
            })

        df = pd.DataFrame(data)
        df.to_csv(filename, sep="\t", index=False)
        print(f"Corpus sauvegardé dans {filename}")

    def load(self, filename):
        df = pd.read_csv(filename, sep="\t")

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

    def afficher_sources(self):
        for doc_id, doc in self.id2doc.items():
            print(f"{doc_id} : {doc.getType()} - {doc.titre}")

    def search(self, mot_cle):
        pattern = re.compile(rf"\b{mot_cle}\b", re.IGNORECASE)
        results = []

        for doc_id, doc in self.id2doc.items():
            if pattern.search(doc.texte):
                results.append((doc_id, doc))

        return results

    def concorde(self, mot_cle, window=30):
        pattern = re.compile(rf"(.{{0,{window}}})\b({mot_cle})\b(.{{0,{window}}})", re.IGNORECASE)
        concordance_list = []

        for doc_id, doc in self.id2doc.items():
            matches = re.findall(pattern, doc.texte)

            for left, mot, right in matches:
                concordance_list.append((left.strip(), mot, right.strip(), doc_id))

        return concordance_list
    
    def nettoyer_texte(self):
        #mise en minuscule , remplacement des passage a la ligne , remplacer les ponctuation et chiffres a l'aide d expression reguliere 
            for doc_id, doc in self.id2doc.items():
                texte = doc.texte.lower()
                texte = texte.replace('\n', ' ').replace('\r', ' ')
                texte = re.sub(r'[^\w\s]', ' ', texte)
                texte = re.sub(r'\d+', ' ', texte)
                texte = re.sub(r'\s+', ' ', texte).strip()
                doc.texte = texte

    def build_vocab(self):
        vocab = set()

        for doc in self.id2doc.values():
            vocab.update(doc.texte.split())

        self.vocab = sorted(vocab)
        return self.vocab

    def term_frequency(self):
        freq = {}

        for doc in self.id2doc.values():
            for mot in doc.texte.split():
                freq[mot] = freq.get(mot, 0) + 1

        return pd.DataFrame.from_dict(freq, orient='index', columns=['term_frequency'])


    
    def document_frequency(self):
        dfreq = {}

        for mot in self.vocab:
            dfreq[mot] = sum(1 for doc in self.id2doc.values() if mot in doc.texte.split())

        return pd.DataFrame.from_dict(dfreq, orient='index', columns=['document_frequency'])
        



    class Corpus:
        _instance = None  # attribut de classe

        def __new__(cls, *args, **kwargs):
            if cls._instance is None:
                cls._instance = super(Corpus, cls).__new__(cls)
            return cls._instance
