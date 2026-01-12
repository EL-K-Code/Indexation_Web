from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

def can_fetch(url, user_agent='*'):

    """
    Verify if the user agent can parsed the data

    Args:
        url (str): The URL to check.
        user_agent (str): The user agent to check for. Default is '*'.
    """

    rp = RobotFileParser()
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp.set_url(robots_url)
    rp.read()
    return rp.can_fetch(user_agent, url)
