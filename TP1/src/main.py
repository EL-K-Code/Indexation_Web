from crawler import crawl


if __name__ == "__main__":
    seed_url = "https://web-scraping.dev/products"
    results = crawl(seed_url)
    for page in results:
        print(page)