import os
import json
from loader import load_all_json_from_dir
from search import search

# --- Load indexes ---
indexes = load_all_json_from_dir("input")

# --- Load corpus ---
with open("rearranged_products.jsonl", "r", encoding="utf-8") as f:
    corpus = [json.loads(line) for line in f]

# --- Stats ---
stats = {
    "N": len(corpus),
    "avg_len": 50,
    "doc_len": {}
}

# --- Test queries ---
test_queries = [
    "beanie",
    "warm winter beanie",
    "dark red beanie",
    "beanie made in usa",
    "pink beanie",
    "grey winter hat"
]

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

doc_lookup = {doc["url"]: doc for doc in corpus}

all_results = []

for query in test_queries:
    scored_results = search(query, indexes, stats)

    formatted = {
        "query": query,
        "total_documents": len(corpus),
        "filtered_documents": len(scored_results),
        "results": []
    }

    for url, score in scored_results:
        doc = doc_lookup.get(url, {})
        formatted["results"].append({
            "title": doc.get("title"),
            "url": url,
            "description": doc.get("description"),
            "score": round(score, 3)
        })

    all_results.append(formatted)

# Save all queries results
with open("output/search_results_all_queries.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, ensure_ascii=False, indent=4)

print("Search results saved to output/search_results_all_queries.json")
