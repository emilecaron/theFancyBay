from scrapy.item import Item, Field

bayDomain = 'thepiratebay.se'
imdbDomain = 'imdb.com'


def absUrl( rel_url, domain=bayDomain):
    return 'http://' + domain + rel_url.pop()

class MovieItem(Item):
    link = Field(input_processor=absUrl)
    magnet = Field() ###
    name = Field()
    seeders = Field()
    leechers = Field()
    
    imdb_url = Field()

    img = Field()
    img_name = Field()
    name_clean = Field() ###

    query = Field()


