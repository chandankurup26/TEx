from text_extractor import extract
from google import genai

#extracting text from source link
news_link = input("Enter link: ")
txt = extract(news_link)

#text cleaning using gemini_ai
client = genai.Client()
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Clean the given text by removing unnecessary symbols or formatting, then convert it into a properly structured title and paragraph format: %s" %txt)

def output():
    return response.text
