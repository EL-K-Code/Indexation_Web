from urllib.request import urlopen, Request

def requeter_url(url):

    try:
        response =urlopen(url)
        if response.getcode() == 200:
            return response.read().decode('utf-8')
        else:
            return "Error: Unable to fetch the URL."
    except:
        return "Error: An exception occurred while fetching the URL."   
    

def request_url_with_headers(url, headers):
    req = Request(url, headers=headers)
    try:
        response = urlopen(req)
        if response.getcode() == 200:
            return response.read().decode('utf-8')
        else:
            return "Error: Unable to fetch the URL with headers."
    except:
        return "Error: An exception occurred while fetching the URL with headers."