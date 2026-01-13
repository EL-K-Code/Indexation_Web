import json
from urllib.parse import urlparse, parse_qs

def load_corpus(path):
    corpus = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            corpus.append(json.loads(line.strip()))
    return corpus


def extract_product_id_and_variant(url):
    parsed = urlparse(url)
    parts = parsed.path.strip("/").split("/")
    product_id = None

    if len(parts) >= 2 and parts[0] == "product":
        product_id = parts[1]

    query_params = parse_qs(parsed.query)
    variant = query_params.get("variant", [None])[0]

    return {
        "product_id": product_id,
        "variant": variant
    } if variant else {
        "product_id": product_id
    }
