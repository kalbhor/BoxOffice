import requests
import json
import omdb
import os
import re
from bs4 import BeautifulSoup

def get_trailer(query):
    """
    Gather all urls of the trailer for a search query
    from youtube
    """

    YOUTUBECLASS = 'spf-prefetch' # Youtube class containing video
    query = "{} {}".format(query,'trailer')
    html = requests.get('https://www.youtube.com/results',
                        params={'search_query': query})
    soup = BeautifulSoup(html.text, 'html.parser')

    soup_section = soup.findAll('a', {'rel': YOUTUBECLASS})

    video_urls = ['https://www.youtube.com' + i.get('href')
                 for i in soup_section]

    return video_urls[0] # Return top result

def get_movie_files(loc='.'):
    """
    Lists out all movie files in nested directories
    """
    VIDEO_FORMATS = ['avi', 'asf', 'mp4', 'mov', 'flv', 'swf', 'mpg', 'wmv']

    movies = [] # List for storing video files
    movie_dirs = {} # Dict storing 'folder' : [movies] 

    for root, dirs, files in os.walk(loc, topdown = True):
        folder = os.path.basename(os.path.normpath(root)) # Folder containing videos
        for file in files:
            if file[-3:] in VIDEO_FORMATS: # Check file format eg : hello.mp4 -> mp4 
                movies.append(file[:-4]) # Append file name eg : hello.mp4 -> hello

        movie_dirs[folder] = movies
        movies = []

    del movies

    return movie_dirs

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


def improve_name(query):
    """
    Improves file name by removing useless words
    """
    try:
        query = os.path.splitext(query)[0]
    except IndexError:
        pass

    # Words to omit from file title for better results
    chars_filter = "()*[]{}-:_/=+\"\'"
    words_filter = ('official', 'subtitles', 'dvd', 'remix', 'video',
                    'full', 'version', 'music', 'mp4', 'hd', 'hq', 
                    'uploaded', 'torrent', 'movie', 'season')

    # Replace characters to filter with spaces
    query = ''.join(map(lambda c: " " if c in chars_filter else c, query))

    # Remove crap words
    query = re.sub('|'.join(re.escape(key) for key in words_filter),
                       "", query, flags=re.IGNORECASE)

    # Remove duplicate spaces
    query = re.sub(' +', ' ', query)

    return query.strip()


if __name__ == '__main__':
    query = input('> ')
    info = get_movie_files(query)
    print(info)


