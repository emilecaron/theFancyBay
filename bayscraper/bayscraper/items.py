from scrapy.item import Item, Field

bayDomain = 'thepiratebay.se'
imdbDomain = 'imdb.com'

# Mettre ailleurs...
def absUrl( rel_url, domain=bayDomain):
    '''
    Input_processor to make [url] -> absolute
    '''
    return 'http://' + domain + rel_url.pop()


class MovieItem(Item):
    link = Field(input_processor=absUrl)
    name = Field()
    seeders = Field()
    leechers = Field()
    img = Field()


