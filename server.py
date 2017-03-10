#!/usr/bin/env python3

from flask import Flask, render_template
import os
import socket
from movietools.movietools import *

app = Flask(__name__)
movies = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("google.com",80))
IP_ADDR = (s.getsockname()[0])
s.close()

def list_movie_files(loc='.'):
	"""
	Lists out all movie files in nested directories
	"""
	movies = []
	for root, dirs, files in os.walk(loc, topdown = True):
		for file in files:
			if file.endswith('.mp4') or file.endswith('.mkv'):
				movies.append(file[:-4])

	trailers = [get_trailer(movie) for movie in movies]
	imdb_info = [get_imdb_info(movie) for movie in movies]

	return movies, trailers, imdb_info
 
@app.route('/')
def home():
    print("Your IP Address : {}".format(IP_ADDR))
    movies, trailers, imdb_info = list_movie_files()
    return render_template('index.html', movies = movies, trailers = trailers, imdb_info = imdb_info)

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0') 
