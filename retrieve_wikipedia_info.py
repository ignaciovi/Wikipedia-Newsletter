import requests
import logging
from datetime import datetime

def retrieve_wikipedia_info():
    '''Retrieve html wikipedia page'''

    
    logging.basicConfig(filename='logs/etl.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.getLogger().setLevel(logging.DEBUG)

    current_date = datetime.now().strftime('%B_%#d')

    url = 'https://en.wikipedia.org/wiki/Wikipedia:Selected_anniversaries/{}'.format(current_date)

    try:
        r = requests.get(url)
    except requests.exceptions.Timeout:
        logging.exception('Request URL Timeout')
    except requests.exceptions.TooManyRedirects:
        logging.exception('Request URL TooManyRedirects')
    except requests.exceptions.RequestException as e:
        logging.exception('Request URL RequestException')
        raise SystemExit(e)

    html_content = str(r.text)

    return html_content

