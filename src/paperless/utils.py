import unicodedata


def make_searchable(content):
    return (
        unicodedata.normalize("NFKD", content.casefold())
        .encode("ASCII", "ignore")
        .decode("utf-8")
    )
