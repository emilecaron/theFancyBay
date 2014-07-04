from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from bayscraper import settings
from bayscraper.spiders.baySpider import BaySpider
from scrapy.settings import Settings
from scrapy.xlib.pydispatch import dispatcher
from threading import Thread
from twisted.internet import reactor, task

class SpiderFarm(object):

    # Scheduled function -> executed on next iteration 
    # TODO: use list to manage simultaneous queries
    f = None

    # static thread
    t = None 

    # Reactor iteration delta (s)
    delta = 1.0

    @classmethod
    def loopRunner( cls,_1=None, _2=None):
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
        print('Scraping Done.')
        print(spider)
        print(spider.query)
        print(reason)
        
        # notify client now....


    @classmethod
    def sendSpider( cls, query='' ):
        """
        Load a BaySpider with its settings + run scrapy
        Returns (scraptime, error)
        """
        # Manage spider thread  
        if cls.t is None :
            print('Starting reactor...')
            l = task.LoopingCall(cls.loopRunner)
            l.start(cls.delta)
            cls.t = Thread(target=reactor.run, args=(False,))
            cls.t.start()
            
        # Create the spider
        spider = BaySpider()
        if query != '':
            print('Making custom search...')
            spider.loadSearch(query)
        spider.callBack(cls.scrapCallback)
        
        # Configure scrapy settings
        ownSettings = get_project_settings()
        ownSettings.setmodule(settings)
        cls.crawler = Crawler(ownSettings)
        cls.crawler.configure()
        cls.crawler.crawl(spider)

        #dispatcher.connect(cls.scrapCallback, signal=signals.spider_closed)
        print('Spider is set up')

        # Schedule spider start
        cls.f = cls.crawler.start
        print('Spider is in the launching ramp')

        return "foo", 0


if __name__=='__main__' :
    SpiderFarm.sendSpider("matrix")
