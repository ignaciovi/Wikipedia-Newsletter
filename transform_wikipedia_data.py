from bs4 import BeautifulSoup

def transform_wikipedia_data(data):
    soup = BeautifulSoup(data, "html.parser")
    div = soup.find('div', {'class': 'mw-parser-output'})
    children = div.findChildren("ul" , recursive=False)
    
    tdTags = children[0].find_all("li")
    output = ""
    for tag in tdTags:
        output = output + tag.text

    return output
