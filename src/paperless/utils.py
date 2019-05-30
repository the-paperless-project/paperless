import unicodedata

def slugify(content):
    return (
        unicodedata.normalize("NFKD", content.casefold())
        .encode("ASCII", "ignore")
        .decode("utf-8")
    )
