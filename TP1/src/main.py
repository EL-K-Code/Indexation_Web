from TP1.src.requests import requeter_url
from TP1.src.robots import can_fetch
from parser import parse_html, extract_titles

url = "https://web-scraping.dev/products"

html_content = requeter_url(url)

user_agent = "MyWebScraperBot"
is_allowed = can_fetch(url, user_agent)
print(f"Can '{user_agent}' fetch '{url}': {is_allowed}")

soup = parse_html(html_content)