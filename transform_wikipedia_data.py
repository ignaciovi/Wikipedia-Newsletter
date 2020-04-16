import logging
from bs4 import BeautifulSoup

def transform_wikipedia_data(data):
    '''Retrieve events from html wikipedia page'''
    
    try: 
        soup = BeautifulSoup(data, 'html.parser')
        div = soup.find('div', {'class': 'mw-parser-output'})
        children = div.findChildren('ul' , recursive=False)
        
        tdTags = children[0].find_all('li')
        output = [tag.text.split(' – ') for tag in tdTags]
    except:
        logging.debug('Error getting URL events')
        return None

    return output
