import requests
import json
import omdb
from bs4 import BeautifulSoup

def get_trailer_url(query):
    """
    Gather all urls of the trailer for a search query
    from youtube
    """

    YOUTUBECLASS = 'spf-prefetch'
    query = "{} {}".format(query,'trailer')
    html = requests.get('https://www.youtube.com/results',
                        params={'search_query': query})
    soup = BeautifulSoup(html.text, 'html.parser')

    soup_section = soup.findAll('a', {'rel': YOUTUBECLASS})

    video_urls = ['https://www.youtube.com' + i.get('href')
                 for i in soup_section]

    return video_urls 

def get_imdb_info(query):
    """
    Gathers all imdb info on a movie/tv show
    """
    search = omdb.search(query)
    imdb_info = {}

    try:
        search = search[0].title
    except IndexError:
        print('An exception occured while searching for query')
    else:
        search_result = omdb.title(search)
        imdb_info = {
            'title' : search_result.title,
            'cast' : search_result.actors,
            'genre' : search_result.genre,
            'plot' : search_result.plot,
            'rating' : search_result.imdb_rating,
            'poster' : search_result.poster,
            'writer' : search_result.writer,
            }
    
    return imdb_info



if __name__ == '__main__':
    query = input('> ')
    info = get_imdb_info(query)
    print(info)


