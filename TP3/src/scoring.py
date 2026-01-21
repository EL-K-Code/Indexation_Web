import math

def bm25_score(tf, df, doc_len, avg_len, N, k1=1.5, b=0.75):
    idf = math.log((N - df + 0.5) / (df + 0.5) + 1)
    return idf * ((tf * (k1 + 1)) / (tf + k1 * (1 - b + b * doc_len / avg_len)))


def exact_match(tokens, doc_url, index):
    return all(doc_url in index.get(t, []) for t in tokens)


def linear_score(doc_url, query_tokens,
                 title_index, desc_index,
                 brand_index, origin_index,
                 review_index, stats):

    score = 0.0

    # --- BM25 / présence texte ---
    for token in query_tokens:
        if doc_url in title_index.get(token, []):
            score += 4    # title = signal fort

        if doc_url in desc_index.get(token, []):
            score += 1    # description = signal plus faible

        # --- BRAND signal ---
        if token in brand_index and doc_url in brand_index[token]:
            score += 2

        # --- ORIGIN signal ---
        if token in origin_index and doc_url in origin_index[token]:
            score += 2

    # --- Exact match boost (titre) ---
    if all(doc_url in title_index.get(t, []) for t in query_tokens):
        score += 7

    # --- Reviews signal ---
    reviews = review_index.get(doc_url)
    if reviews:
        score += 2 * reviews.get("mean_mark", 0)
        score += math.log(1 + reviews.get("total_reviews", 0))

    return score

