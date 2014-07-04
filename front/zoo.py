from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from bayscraper import settings
from bayscraper.spiders.baySpider import BaySpider
from scrapy.settings import Settings
from scrapy.xlib.pydispatch import dispatcher

from twisted.internet import reactor, task

class SpiderFarm(object):

    # Scheduled function -> executed on next iteration 
    # TODO: use list to manage simultaneous queries
    f = None

    # static thread
    t = None 

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
    def scrapCallback( cls ):
        """
        Called on spider shutdown.
        Might work, eventually
        """
        print('Scraping Done.')


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
            #l.start(5.0)
            l.start(5.0)
            from threading import Thread
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
        print('Spider is set up')

        # Schedule spider start
        cls.f = cls.crawler.start
        print('Spider is in the launching ramp')

        return "foo", 0


if __name__=='__main__' :
    SpiderFarm.sendSpider("matrix")
