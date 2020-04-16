import requests
from datetime import datetime

def retrieve_wikipedia_info():
    '''Retrieve html wikipedia page'''

    current_date = datetime.now().strftime('%B_%#d')

    url = 'https://en.wikipedia.org/wiki/Wikipedia:Selected_anniversaries/{}'.format(current_date)

    try:
        r = requests.get(url)
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
    except requests.exceptions.RequestException as e:
        logging.debug('')
        raise SystemExit(e)

    html_content = str(r.text)

    return html_content

