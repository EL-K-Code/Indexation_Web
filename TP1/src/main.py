from crawler_ import Crawler
crawler = Crawler("https://web-scraping.dev/product/12")
corpus = crawler.crawl()

corpus_file = "./output/corpus.json"
with open(corpus_file, "w", encoding="utf-8") as f:
    import json
    json.dump(corpus, f, ensure_ascii=False, indent=4)  