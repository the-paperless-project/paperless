import re

from .parsers import PdfDocumentParser


class ConsumerDeclaration:

    MATCHING_FILES = re.compile(r"^.*\.(pdf|jpe?g)$")

    @classmethod
    def handle(cls, sender, **kwargs):
        return cls.test

    @classmethod
    def test(cls, doc):

        if cls.MATCHING_FILES.match(doc.lower()):
            return {
                "parser": PdfDocumentParser,
                "weight": 10
            }

        return None
