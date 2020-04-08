from bs4 import BeautifulSoup
import re

def transform_wikipedia_data(data):
    soup = BeautifulSoup(data, "html.parser")
    div = soup.find('div', {'class': 'mw-parser-output'})
    children = div.findChildren("ul" , recursive=False)
    
    tdTags = children[0].find_all("li")
    output = [tag.text.split(" – ") for tag in tdTags]

    return output
