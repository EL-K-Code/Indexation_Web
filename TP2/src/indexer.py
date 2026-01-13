from inverted_index import build_positional_index, build_feature_index, review_index

class Indexer:
    def __init__(self, corpus):
        self.corpus = corpus

        self.title_index = {}
        self.description_index = {}
        self.title_positional_index = {}
        self.description_positional_index = {}
        self.feature_indexes = {}
        self.review_index = {}

    def build_text_indexes(self):
        self.title_index = build_positional_index(self.corpus, "title")
        self.description_index = build_positional_index(self.corpus, "description")

    def build_feature_index(self, feature_name):
        self.feature_indexes[feature_name] = build_feature_index(
            self.corpus, feature_name
        )

    def build_review_index(self):
        for doc in self.corpus:
            self.review_index.update(review_index(doc))

    def save_indexes(self, output_dir="../indexes"):
        import os, json
        os.makedirs(output_dir, exist_ok=True)

        indexes = {
            "title_index": self.title_index,
            "description_index": self.description_index,
            "review_index": self.review_index,
            **self.feature_indexes
        }

        for name, index in indexes.items():
            with open(f"{output_dir}/{name}.json", "w", encoding="utf-8") as f:
                json.dump(index, f, indent=2, ensure_ascii=False)
