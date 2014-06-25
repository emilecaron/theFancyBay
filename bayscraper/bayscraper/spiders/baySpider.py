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
        urll = Selector(response).xpath('//a[contains(@href,"{}")]/@href'.format(imdbDomain)).extract()
        if urll :
            url = urll.pop()
            r =  Request( url, self.parseMovieImdb)
            item = response.meta['item']
            item['imdb_url']=url
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


