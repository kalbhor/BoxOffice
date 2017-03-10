import requests
import json
import omdb
from bs4 import BeautifulSoup

def get_trailer(query):
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

    return video_urls[0]

def get_movie_files(loc='.'):
    """
    Lists out all movie files in nested directories
    """
    movies = []
    for root, dirs, files in os.walk(loc, topdown = True):
        for file in files:
            if file.endswith('.mp4') or file.endswith('.mkv'):
                movies.append(file[:-4])
                
    return movies

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
    info = get_trailer(query)
    print(info)


