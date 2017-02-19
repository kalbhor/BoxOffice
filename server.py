from flask import Flask, render_template
import os
import socket


app = Flask(__name__)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("google.com",80))
IP_ADDR = (s.getsockname()[0])
s.close()
 
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
   app.run(debug=True, host = '0.0.0.0') 
