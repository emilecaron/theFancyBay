theFancyBay
===========
Because piratebay isn't so fancy...

![preview](http://github.com/emilecaron/theFancyBay/blob/master/fancyBay.png)

Get Started
-----------
Install required dependencies using pip::

    $ pip install Scrapy Flask Flask-Sockets requests gunicorn
  
Run the dev server with the provided script::
    
    $ cd front && ./memo_gunicorn
    
The site should be available on port 8000. 


Features
-----------
Browse a enhanced version of piratebay that will only display movies with a valid [IMDB](http://imdb.org) link. Scrapy will crawl the search page and extract all useful data (links, seed, leech) then will jump to imdb to retrieve the image. Results will show up on the page as soon as they are found using a websocket for communication. Custom searches are supported.

The server will only store images to prevent hotlinking to imdb.org, nothing else is stored, no database is required.


Technologies
-----------
[Flask](http://flask.readthedocs.org/en/latest/), 
[Flask_websockets](https://github.com/kennethreitz/flask-sockets), 
[Scrapy](http://scrapy.org/), 
[Bootstrap](http://getbootstrap.com/),
Jquery,
Underscore 

