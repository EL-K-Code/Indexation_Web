from indexer import Indexer
from utils import load_corpus


corpus = load_corpus("../input/products_enriched.jsonl")

indexer = Indexer(corpus)

indexer.build_text_indexes()
indexer.build_feature_index("brand")
indexer.build_feature_index("made in")
indexer.build_review_index()
indexer.save_indexes()
