import re

from .parsers import TikaDocumentParser


class ConsumerDeclaration:

    MATCHING_FILES = re.compile(r"^.*\.(ods|odt|odp|xlsx?|docx?|pptx?)$")

    @classmethod
    def handle(cls, sender, **kwargs):
        return cls.test

    @classmethod
    def test(cls, doc):

        if cls.MATCHING_FILES.match(doc.lower()):
            return {
                "parser": TikaDocumentParser,
                "weight": 10
            }

        return None
