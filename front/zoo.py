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
    f = None

    # static thread
    t = None 

    @classmethod
    def loopRunner( cls,_1=None, _2=None):
        #print('Mission is complete')
        #print(_1)
        #print(_2)
        if cls.f !=None:
            print('crawler.start()')
            b = cls.f
            cls.f= None
            b()

    @classmethod
    def scrapCallback( cls ):
        print('Scraping Done.')


    @classmethod
    def sendSpider( cls, query='' ):
        """
        Load a BaySpider with its settings + run scrapy
        Returns (scraptime, error)
        """
        # start a thread if static t is None
        if cls.t is None :
            print('Starting reactor...')
            l = task.LoopingCall(cls.loopRunner)
            #l.start(5.0)
            l.start(5.0)
            from threading import Thread
            cls.t = Thread(target=reactor.run, args=(False,))
            cls.t.start()


        spider = BaySpider()
        if query != '':
            print('Making custom search...')
            spider.loadSearch(query)
        spider.callBack(cls.scrapCallback)
        ownSettings = get_project_settings()
        ownSettings.setmodule(settings)
        cls.crawler = Crawler(ownSettings)
        cls.crawler.configure()
        cls.crawler.crawl(spider)
        print('Spider ready...')
        #d.addCallback(missionComplete)
        try :
            pass
            #cls.crawler.signals.connect(cls.missionComplete, signals.engine_stopped)
            #dispatcher.connect(cls.missionComplete, signals.spider_closed)
        except:
            pass
        #log.start(loglevel=log.DEBUG)
        #log.start()
        #d = cls.crawler.start()
        cls.f = cls.crawler.start
        #import time
        #time.sleep(10)
        #log.start()
        print('Spider sent...')
        #return d
        return "foo", 0


if __name__=='__main__' :
    SpiderFarm.sendSpider("matrix")
