import requests
import json
from bs4 import BeautifulSoup

YOUTUBECLASS = 'spf-prefetch'

def get_trailer_url(query):
    """
    Gather all urls of the trailer for a search query
    from youtube
    """
    query = "{} {}".format(query,'trailer')
    html = requests.get('https://www.youtube.com/results',
                        params={'search_query': query})
    soup = BeautifulSoup(html.text, 'html.parser')

    soup_section = soup.findAll('a', {'rel': YOUTUBECLASS})

    video_urls = ['https://www.youtube.com' + i.get('href')
                 for i in soup_section]

    return video_urls 

