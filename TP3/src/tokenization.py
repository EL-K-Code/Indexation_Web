import json
import spacy
from nltk.corpus import stopwords

nlp = spacy.load("en_core_web_sm")
STOPWORDS = set(stopwords.words("english"))


def tokenize(text: str):
    """
    Tokenize and normalize a text:
    - lowercase
    - lemmatization
    - remove punctuation, numbers, stopwords
    """

    if not text:
        return []

    doc = nlp(text)
    tokens = []

    for tok in doc:
        if tok.is_punct or tok.is_space:
            continue
        if not tok.is_alpha:
            continue

        lemma = tok.lemma_.lower()

        if lemma in STOPWORDS:
            continue

        tokens.append(lemma)

    return tokens


def expand_country_synonyms(tokens, synonyms_path="input/origin_synonyms.json"):
    """
    Expand query tokens using country/origin synonyms.
    Example: 'usa' → 'united_states', 'america'
    """

    try:
        with open(synonyms_path, "r", encoding="utf-8") as f:
            synonyms = json.load(f)
    except FileNotFoundError:
        return tokens

    expanded_tokens = set(tokens)
    joined_text = " ".join(tokens)

    for canonical, variants in synonyms.items():
        for v in variants:
            if v in joined_text:
                expanded_tokens.add(canonical)

    return list(expanded_tokens)


def process_query(query: str):
    """
    Full query processing pipeline:
    - tokenization
    - normalization
    - stopword removal (NLTK)
    - synonym-based query expansion (countries)
    """

    tokens = tokenize(query)
    tokens = expand_country_synonyms(tokens)

    tokens = list(dict.fromkeys(tokens))

    return tokens
