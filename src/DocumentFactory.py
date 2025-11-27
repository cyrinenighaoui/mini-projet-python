from RedditDocument import RedditDocument
from ArxivDocument import ArxivDocument
from document import Document

class DocumentFactory:

    def create_document(self, doc_type, *args, **kwargs):
        if doc_type == "reddit":
            return RedditDocument(*args, **kwargs)
        elif doc_type == "arxiv":
            return ArxivDocument(*args, **kwargs)
        else:
            return Document(*args, **kwargs)
