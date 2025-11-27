from document import Document

class ArxivDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, co_auteurs):
        super().__init__(titre, auteur, date, url, texte)
        self.co_auteurs = co_auteurs
        self.type = "Arxiv"

    def get_co_auteurs(self):
        return self.co_auteurs

    def set_co_auteurs(self, co_auteurs):
        self.co_auteurs = co_auteurs

    def __str__(self):
        liste = ", ".join(self.co_auteurs) if self.co_auteurs else "Aucun"
        return f"[Arxiv] {self.titre} - Co-auteurs : {liste}"
