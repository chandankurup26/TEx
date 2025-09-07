from bs4 import BeautifulSoup
import requests

def extract(url):
    full_text = ""
    text_parts = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # finding all header elements
    headers = soup.find_all("h1")

    #finding all paragraph elements
    paragraphs = soup.find_all("p")

    # extract and showing text from each paragraph
    for header in headers:
        text_parts.append(header.get_text())

    #extract and showing text from each paragraph
    for paragraph in paragraphs:
        text_parts.append(paragraph.get_text())

    full_text = "\n".join(text_parts)
    return full_text