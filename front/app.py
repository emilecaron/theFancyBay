from flask import Flask, render_template, url_for, send_from_directory#, json
from os import path
import requests
import zoo
from flask_sockets import Sockets


# create the application object
app = Flask(__name__)
app.config.from_object(__name__)
sockets = Sockets(app)


@sockets.route('/socket')
def echo_socket(ws):
    while True:
        query = ws.receive()
        time, err = zoo.SpiderFarm.sendSpider( query, pipe=ws.send )    


@app.route('/')
def socketpage():
    return render_template('home.html')


@app.route('/cache/<path:img>')
def get_img(img):
    '''
    Cache imdb images (imdb dont like no hotlinking...)
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
    print('See provided \'memo_gunicorn\' to launch app with websocket support')
