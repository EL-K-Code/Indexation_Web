from collections import deque
from urllib.parse import urlparse
from TP1.src.requests import requeter_url
from TP1.src.robots import can_fetch
from TP1.src.parser import parse_html, extract_infos

MAX_PAGES = 50
TOKEN = "product"

def crawl(seed_url):
    base_domain = urlparse(seed_url).netloc

    priority_queue = deque([seed_url])
    normal_queue = deque()
    visited = set()

    results = []

    while (priority_queue or normal_queue) and len(visited) < MAX_PAGES:
        if priority_queue:
            url = priority_queue.popleft()
        else:
            url = normal_queue.popleft()

        if url in visited:
            continue

        print(f"[{len(visited)+1}/{MAX_PAGES}] Crawling:", url)
        visited.add(url)

        html = requeter_url(url)
        if not html:
            continue

        page_data = extract_infos(parse_html(html), url)
        results.append(page_data)

        for link in page_data["links"]:
            if link in visited:
                continue

            if urlparse(link).netloc != base_domain:
                continue

            if TOKEN in link:
                priority_queue.append(link)
            else:
                normal_queue.append(link)

    return results
