from pymongo import Connection

connection = Connection('localhost', 27017)
db = connection.moviesdb
#db['movies'].remove({}) #temporary hack - delete all records

class BayPipeline(object):
    """
    Custom pipeline to store items in a mongodb
    """
    def process_item(self, item, spider):
        db['movies'].insert(dict(item))
        return item
