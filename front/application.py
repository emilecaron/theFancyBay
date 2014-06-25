
#import json
from flask import Flask, render_template, url_for, send_from_directory
from flask_debugtoolbar import DebugToolbarExtension
from pymongo import Connection
from os import path
import requests

app = Flask(__name__)
connection = Connection('localhost', 27017) 
db = connection.moviesdb

@app.route('/')
def show_index():
    jsn = [{'img':'8==D.png','name':'mabitelefilm'},
        {'img':'xxx.png','name':'poneyMoviz'}]

    
    #jsn = json.load(open('x.json','r'))
    dat = db['movies'].find()
    
    return render_template('show_movies.html', movies=dat)

def update_cache( data ):
    """
    Prevent hot linking because imdb fait la tronche
    """
    for movie in data :
        url = zob

@app.route('/cache/<path:img>')
def get_img(img):
    '''
    Cache system for images
    '''
    if not path.isfile('cache/'+img):
        # query and store
        url = 'http://ia.media-imdb.com/images/M/' + img
        local_filename = path.join('cache', img)
        try :
            r = requests.get(url, stream=True)
        except requests.ConnectionError:
            return 
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk:
                    f.write(chunk)
                    f.flush()
    
    return send_from_directory('cache',img) 


if __name__=="__main__" :
    toolbar = DebugToolbarExtension(app)
    app.debug = True
    app.run(host="0.0.0.0")
