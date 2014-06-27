from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.xlib.pydispatch import dispatcher
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from bayscraper import settings
from bayscraper.spiders.baySpider import BaySpider
from scrapy.settings import Settings
import time

def sendSpider( query='' ):
    """
    Load a BaySpider with its settings + run scrapy
    Returns (scraptime, error)
    """
    #TODO : use thread instead of reactor/dispatcher
    spider = BaySpider()
    if query != '':
        print('Making custom search...')
        spider.loadSearch(query)
    ownSettings = get_project_settings()
    ownSettings.setmodule(settings)
    crawler = Crawler(ownSettings)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    try :
        dispatcher.connect(reactor.stop, signal=signals.spider_closed)
    except Exception as e:
        print(e)
        exit(1)

    log.start(loglevel=log.DEBUG)
    print('Spider sent...')
    t0 = time.time()
    reactor.run(False)
    d = round(time.time()-t0, 3)
    error = 0

    return d, error
    return 'running...', 0

if __name__=='__main__' :
    print( '{}s'.format(sendSpider(raw_input('Search TPB >'))[0]))

