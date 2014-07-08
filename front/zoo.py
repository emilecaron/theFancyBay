from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from bayscraper import settings
from bayscraper.spiders.baySpider import BaySpider
from scrapy.settings import Settings
from scrapy.xlib.pydispatch import dispatcher
from threading import Thread
from twisted.internet import reactor, task
import time
import json

class SpiderFarm(object):

    # Scheduled function -> executed on next iteration 
    # TODO: use list to manage simultaneous queries
    f = None

    # static thread
    t = None 

    # Reactor iteration delta (s)
    delta = 1.0

    @classmethod
    #def loopRunner( cls,_1=None, _2=None):
    def loopRunner( cls):
        """
        Called on every reactor iteration
        Triggers the functions in cls.f
        """
        if cls.f !=None:
            print('crawler.start()')
            b = cls.f
            cls.f= None
            b()

    @classmethod
    def scrapCallback( cls, spider, reason ):
        """
        Called on spider shutdown.
        Might work, eventually
        """
        print('Scraping Done (reason="{}", search="{}")'.format(reason,spider.query))
        cls.sync = False


    @classmethod
    def sendSpider( cls, query='', pipe=None, sync=False):
        """
        Load a BaySpider with its settings + run scrapy
        Query is searched movie
        pipe is function to call for each item scrapped
        sync: async / sync function
        Returns (scraptime, error)
        """
        def progress(msg, val):
            """ Send progress info to client """
            if pipe:
                dat = {'control': {'msg':msg,'val' : val}}
                pipe(json.dumps(dat))

        # TODO class variable = not good at all, find something else....
        cls.sync = sync

        # Manage spider thread  
        progress('Starting reactor', 0)
        if cls.t is None :
            print('Starting reactor...')
            l = task.LoopingCall(cls.loopRunner)
            l.start(cls.delta)
            cls.t = Thread(target=reactor.run, args=(False,))
            cls.t.start()
            
        # Create the spider
        progress('Creating spider', 0)
        spider = BaySpider()
        spider.loadStartUrl(search=query)

        # bind callbacks
        spider.callBack(cls.scrapCallback)
        spider.setItemPipe( pipe )

        # Configure crawler settings
        cls.crawler = Crawler( Settings()) # pipeline not needed anymore...
        cls.crawler.configure()
        cls.crawler.crawl(spider)
        print('Spider is set up')

        # Schedule spider start
        progress('Scheduling spider', 0)
        cls.f = cls.crawler.start
        print('Spider is in the launching ramp')

        # use for spider debug only
        #log.start(logfile='spider.log',logstdout=None)

        while cls.sync:
            # wait for callback...
            time.sleep(0.1)

        return "foo", 0 #TODO implement dat


if __name__=='__main__' :
    SpiderFarm.sendSpider("matrix")
