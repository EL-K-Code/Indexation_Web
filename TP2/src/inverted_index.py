import spacy
from collections import defaultdict
import string


nlp = spacy.load("en_core_web_sm")


def normalize_feature_value(text):
    if not text:
        return None

    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text.strip()


def tokenize_with_positions(text):
    if not text:
        return []

    doc = nlp(text)
    tokens = []
    pos = 0

    for tok in doc:
        if tok.is_stop or tok.is_punct or tok.is_space:
            continue
        if not tok.is_alpha:
            continue

        tokens.append((tok.lemma_.lower(), pos))
        pos += 1

    return tokens


def build_positional_index(corpus, field):
    index = defaultdict(lambda: defaultdict(list))

    for doc in corpus:
        url = doc["url"]
        text = doc.get(field, "")

        for token, position in tokenize_with_positions(text):
            index[token][url].append(position)

    return {
        token: dict(postings)
        for token, postings in index.items()
    }

def review_index(data):
    output = {
    "total_reviews": 0,
    "mean_mark": 0,
    "last_rating": 0
             }

    if data.get("product_reviews", []):
        total_marks = sum(review.get("rating", 0) for review in data.get("product_reviews", []))
        total_reviews = len(data.get("product_reviews", []))
        mean_mark = total_marks / total_reviews if total_reviews > 0 else 0
        last_rating = data.get("product_reviews", [])[-1].get("rating", 0) if total_reviews > 0 else 0
        output["total_reviews"] = total_reviews
        output["mean_mark"] = mean_mark
        output["last_rating"] = last_rating

    return {data.get("url", ""): output}

def build_feature_index(corpus, feature_name):
    """
    Build an inverted index for a given product feature.

    Args:
        corpus (list): list of product documents
        feature_name (str): e.g. 'brand', 'made in'

    Returns:
        dict: {feature_value: [product_ids]}
    """
    index = defaultdict(set)

    for doc in corpus:
        doc_id = doc.get("url")
        features = doc.get("product_features", {})

        if feature_name not in features:
            continue

        value = normalize_feature_value(features[feature_name])
        if value:
            index[value].add(doc_id)

    return {k: list(v) for k, v in index.items()}
