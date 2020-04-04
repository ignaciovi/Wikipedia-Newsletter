#!/usr/bin/env python
# coding: utf-8

# In[2]:


from bs4 import BeautifulSoup
import requests
from datetime import datetime

def retrieve_wikipedia_info():
    current_date = datetime.now().strftime('%B_%#d')

    url="https://en.wikipedia.org/wiki/Wikipedia:Selected_anniversaries/{}".format(current_date)

    html_content = requests.get(url).text

    html_content_format = str(html_content.encode('utf8'))

    # Add error handling?

    return html_content_format

