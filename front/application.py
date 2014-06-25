
#import json
from flask import Flask, render_template, url_for
from flask_debugtoolbar import DebugToolbarExtension
from pymongo import Connection

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

if __name__=="__main__" :
    toolbar = DebugToolbarExtension(app)
    app.debug = True
    app.run(host="0.0.0.0")
