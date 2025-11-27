from document import Document

class RedditDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, nb_comments):
        super().__init__(titre, auteur, date, url, texte)
        self.nb_comments = nb_comments
        self.type = "Reddit"

    def get_nb_comments(self):
        return self.nb_comments

    def set_nb_comments(self, nb_comments):
        self.nb_comments = nb_comments

    def __str__(self):
        return f"[Reddit] {self.titre} - {self.nb_comments} commentaires"

