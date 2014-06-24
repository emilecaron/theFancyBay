from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy import log
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Join
from scrapy.http import Request

from bayscraper.items import MovieItem, bayDomain, imdbDomain

class BaySpider(Spider):
    """
    PirateBay result page -> Piratebay Torrent Page -> Imdb Page
    """
    name = "BaySpider"
    allowed_domains = [ bayDomain, imdbDomain]
    start_urls = ['http://{}/top/201'.format(bayDomain)]

    # static
    #item_Buffer = {}
    

    def parse(self, response):
        """
        Parse PirateBay Result page
        """
        items = [] # put static ?
        requests = [] 

        xpaths = {
            'name'      : 'td/div[@class="detName"]/a/text()',
            'link'  : 'td/div[@class="detName"]/a/@href',
            'seeders'   : 'td[position()=3]/text()',
            'leechers'  : 'td[position()=3]/text()',
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
                #r.meta['key'] = link
                r.meta['item'] = l.load_item()
                #BaySpider.item_Buffer[link] = l.load_item()
                requests.append(r)

            except Exception as e :
                self.log('Failed extraction for row {}'.format(row))
                raise e # Until prod
                continue    

        return requests
        


    def parseMoviePage(self, response):
        """
        Extract imdb link and request.
        Movies with no links are dropped
        """
        url = Selector(response).xpath('//a[contains(@href,"{}")]/@href'.format(imdbDomain)).extract()
        if url :
            r =  Request( url.pop(), self.parseMovieImdb)
            r.meta['item'] = response.meta['item']
            return r
        self.log('No Imdb for ' + response.meta['item']['name'])

    def parseMovieImdb(self, response):
        item = response.meta['item']
        sel = Selector(response)
        expr = '//img[contains(@alt, "Poster") and substring-after(@alt, "Poster")=""]/@src' 
        img = sel.xpath(expr).extract()

        if img :
            item['img'] = img.pop()
            return item
        else :    
            self.log('No image for ' + item['name'])


