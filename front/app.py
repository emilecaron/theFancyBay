from flask import Flask, render_template, url_for, send_from_directory, json
from os import path
import requests
import zoo
import time
from mongokit import Connection, ConnectionError
from flask_sockets import Sockets

#configuration
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

# create the application object
app = Flask(__name__)
app.config.from_object(__name__)
sockets = Sockets(app)

# connect to the database
try :
    con = Connection( app.config['MONGODB_HOST'],
                      app.config['MONGODB_PORT'])
except Exception:
    print('Couldn\'t connect to mongo db. Exiting...')
    exit(1)
    
db = con.moviesdb

### SOCKETS (beta) #################################################

@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        #time.sleep(1)

        dat = db['movies'].find()[0]
        dat['_id'] = '' #dirtyfix
        
        print('json=')
        print(dat)
        ws.send(json.dumps(dat))

@app.route('/socket')
def socketpage():
    return render_template('socket.html')

### ROUTING ########################################################

@app.route('/')
def show_index():
    dat = db['movies'].find()
    return render_template('show_movies.html', movies=dat)

@app.route('/scrap')
@app.route('/scrap/<query>')
def scrap(query=''):
    print('\n\n'+'='*30+'\nDealing with query')
    time, err = zoo.SpiderFarm.sendSpider(query)
    return 'Scrapped in {} seconds. Easy.<a href="/">Results</a>'.format(time)


@app.route('/cache/<path:img>')
def get_img(img):
    '''
    Cache imdb images to prevent hotlinks
    '''
    if not path.isfile('cache/'+img):
        # query and store
        url = 'http://ia.media-imdb.com/images/M/' + img
        local_filename = path.join('cache', img)
        
        r, rem = None, 5
        while r==None and rem:
            rem -= 1
            try :
                r = requests.get(url, stream=True)
            except requests.ConnectionError as e:
                print('\n\n\nImage error for url({}): {}'.format(5-rem, url))
                print('\n\n\n')
                time.sleep(0.1)
                continue
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024): 
                    if chunk:
                        f.write(chunk)
                        f.flush()
        if r == None :
            return send_from_directory('static','error.jpg')
    
    return send_from_directory('cache',img) 


if __name__=="__main__" :
    app.debug = True
    app.run(host="0.0.0.0")
