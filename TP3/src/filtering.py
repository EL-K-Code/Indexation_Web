import os
import json
import nltk
from nltk.corpus import stopwords
from tokenization import tokenize
STOPWORDS = set(stopwords.words("english"))


def load_all_json_from_dir(directory):
    data = {}

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            path = os.path.join(directory, filename)
            with open(path, "r", encoding="utf-8") as f:
                data[filename] = json.load(f)

    return data

indexes = load_all_json_from_dir("input")

title_index = indexes["title_index.json"]
review_index = indexes["reviews_index.json"]
description_index = indexes["description_index.json"]


def filter_docs_at_least_one_token(query_tokens, inverted_index):
    results = set()

    for token in query_tokens:
        if token in STOPWORDS:
            continue

        results.update(inverted_index.get(token, []))

    return list(results)


def filter_docs_all_tokens_except_stopwords(query_tokens, inverted_index):
    doc_sets = []

    for token in query_tokens:
        if token in STOPWORDS:
            continue

        doc_sets.append(set(inverted_index.get(token, [])))

    if not doc_sets:
        return []

    return list(set.intersection(*doc_sets))

