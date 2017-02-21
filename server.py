#!/usr/bin/env python3

from flask import Flask, render_template
import os
import socket


app = Flask(__name__)
movies = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("google.com",80))
IP_ADDR = (s.getsockname()[0])
s.close()

for root, dirs, files in os.walk(".", topdown = True):
	for file in files:
		if file.endswith('.mp4'):
			movies.append(os.path.join(root, file))
 
@app.route('/')
def home():
    return render_template('index.html', movies = movies)

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0') 
