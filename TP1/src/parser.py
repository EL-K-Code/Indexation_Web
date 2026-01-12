from bs4 import BeautifulSoup

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

