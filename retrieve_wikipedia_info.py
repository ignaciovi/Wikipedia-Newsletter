import requests
from datetime import datetime

def retrieve_wikipedia_info():
    '''Retrieve html wikipedia page'''

    current_date = datetime.now().strftime('%B_%#d')

    url="https://en.wikipedia.org/wiki/Wikipedia:Selected_anniversaries/{}".format(current_date)

    html_content = requests.get(url).text

    html_content_format = str(html_content)

    return html_content_format

