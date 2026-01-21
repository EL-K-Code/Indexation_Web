from filtering import (
    filter_docs_all_tokens_except_stopwords,
    filter_docs_at_least_one_token
)
from tokenization import process_query


from scoring import linear_score

def search(query, indexes, stats):
    query_tokens = process_query(query)

    title_index = indexes["title_index.json"]
    description_index = indexes["description_index.json"]
    review_index = indexes["reviews_index.json"]
    brand_index = indexes["brand_index.json"]
    origin_index = indexes["origin_index.json"]

    candidates = filter_docs_all_tokens_except_stopwords(query_tokens, title_index)
    if not candidates:
        candidates = filter_docs_at_least_one_token(query_tokens, title_index)

    results = []
    for doc in candidates:
        score = linear_score(
            doc, query_tokens,
            title_index, description_index,brand_index,origin_index,
            review_index, stats
        )
        results.append((doc, score))

    return sorted(results, key=lambda x: x[1], reverse=True)
