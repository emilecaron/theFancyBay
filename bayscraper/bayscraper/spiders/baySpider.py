from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy import log, signals
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Join
from scrapy.http import Request
from scrapy.xlib.pydispatch import dispatcher
from bayscraper.items import MovieItem, bayDomain, imdbDomain
import json

class BessifSpider(Spider):
    """
    Custom Spider with embedded callback and simple item json output
    """

    def __init__(self):
        raise NotImplementedError

    def callBack(self, mtd):
        """
        Add a function to call on spider closing
        Its parameters must be (spider, reason) 
        """
        dispatcher.connect(mtd, signal=signals.spider_closed)
        #TODO : disconnect ???


    def setItemPipe( self, mtd ):
        """
        Add a function to pass item json to when item is scraped
        + connect signal to its handler
        """
        self.pipe = mtd
        dispatcher.connect(self.item_scraped_handler, signal=signals.item_scraped)

    def item_scraped_handler(self, item):
        """
        Jsonify item and send to pipe
        """
        if item :
            self.pipe(json.dumps(dict(item)))
        


class BaySpider(BessifSpider):
    """
    PirateBay result page -> Piratebay Torrent Page -> Imdb Page
    """
    name = "BaySpider"
    allowed_domains = [ bayDomain, imdbDomain]
    start_urls = [] 

    def __init__(self):
        pass

    def loadStartUrl(self, search):
        """
        Build and set start url from search
        """
        url = 'http://{}/top/201'.format(bayDomain)
        if search :
            url = 'http://{}/search/{}/0/99/200'.format(bayDomain, search)
        BaySpider.start_urls = [ url ]
        self.query=search


    def parse(self, response):
        """
        Parse PirateBay Result page
        """
        requests = [] 

        xpaths = {
            'name'      : 'td/div[@class="detName"]/a/text()',
            'link'  : 'td/div[@class="detName"]/a/@href',
            'seeders'   : 'td[position()=3]/text()',
            'leechers'  : 'td[position()=4]/text()',
            'magnet'    :  'td/a[starts-with(@href, "magnet")]/@href'
        }

        for row in Selector(response).xpath('//tr[not(@class)]'): 
            try :
                l = ItemLoader( MovieItem(), row)
                l.default_output_processor = Join()
                l.default_input_processor = Join()
                
                for key, xpath in xpaths.iteritems():
                   l.add_xpath(key, xpath)

                link = l.get_output_value('link')
                r = Request( link, self.parseMoviePage)
                r.meta['item'] = l.load_item()
                requests.append(r)

            except Exception as e :
                self.log('Failed extraction for row {}'.format(row))
                raise e # TODO dd dat line
                continue    

        return requests
        


    def parseMoviePage(self, response):
        """
        Extract imdb link and request.
        Movies with no links are dropped
        """
        self.log('parseMoviePage')
        urll = Selector(response).xpath('//a[contains(@href,"{}")]/@href'.format(imdbDomain)).extract()
        if urll :
            url = urll.pop().strip('\n ')
            r = Request(url=url, callback=self.parseMovieImdb,dont_filter=True) 
            item = response.meta['item']
            item['imdb_url']=url
            item['query']=self.query
            r.meta['item'] = item
            return r

        self.log('No Imdb for ' + response.meta['item']['name'])

    def parseMovieImdb(self, response):
        """
        Retrieve image path and return item
        Movies with no image are dropped
        """
        item = response.meta['item']
        sel = Selector(response)
        imgx = '//img[contains(@alt, "Poster") and substring-after(@alt, "Poster")=""]/@src' 
        namex = '//h1[@class="header"]/span[@itemprop="name"]/text()'
        img = sel.xpath(imgx).extract()
        name= sel.xpath(namex).extract().pop()

        if img :
            item['img'] = img[0]
            item['img_name'] = img[0].split('/')[-1]
            item['name_clean'] = name
            return item
        else :    
            self.log('No image for ' + name)


