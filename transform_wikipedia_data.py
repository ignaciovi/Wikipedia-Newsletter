import logging
from bs4 import BeautifulSoup

def transform_wikipedia_data(data):
    '''Retrieve events from html wikipedia page'''

    logging.basicConfig(filename='logs/etl.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.getLogger().setLevel(logging.DEBUG)
    
    try: 
        soup = BeautifulSoup(data, 'html.parser')
        div = soup.find('div', {'class': 'mw-parser-output'})
        children = div.findChildren('ul' , recursive=False)
        
        tdTags = children[0].find_all('li')
        output = [tag.text.split(' – ') for tag in tdTags]
    except:
        logging.exception('Error getting URL events')
        return None

    return output
