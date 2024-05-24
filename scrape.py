from bs4 import BeautifulSoup

def extract_text(html_doc:str):
    return BeautifulSoup(html_doc , "html.parser").get_text().strip()

# resp = requests.get("https://en.wikipedia.org/wiki/Luke_Skywalker")
# html_doc=resp.text
# print(type(html_doc))
# soup = BeautifulSoup(html_doc , "html.parser")
# extracted_text = soup.get_text().strip()