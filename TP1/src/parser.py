from bs4 import BeautifulSoup
from urllib.parse import urljoin

def parse_html(html_content):
    """
    Parse the HTML content and return a BeautifulSoup object.

    Args:
        html_content (str): The HTML content to parse.  
    Returns:
        BeautifulSoup: Parsed HTML content.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup


def extract_infos(soup, url=""):
    """
    Extract specific information from the BeautifulSoup object.

    Args:
        soup (BeautifulSoup): The parsed HTML content.  
        url (str): The URL of the page being parsed.
    Returns:
        dict: A dictionary containing extracted information.
    """
    infos = {"url": url, "title": None, "description": "", "links": [""]}
    h3 = soup.find("h3", class_="product-title")
    infos["title"] = h3.get_text(strip=True) if h3 else soup.title.get_text(strip=True)
    first_p = soup.find('p')
    infos["description"] = first_p.get_text() if first_p else None
    for link in soup.find_all('a', href=True):
        href = link['href']
        full_url = urljoin(url, href)
        if full_url not in infos["links"]:
            infos["links"].append(full_url)

    try:
        tables = soup.select("table.table-product")
        features_table = tables[0] 
        for row in features_table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) == 2:
                key = cells[0].get_text(strip=True)
            value = cells[1].get_text(strip=True)
            infos["product_features"][key] = value
    except Exception as e:
        pass
    return infos    