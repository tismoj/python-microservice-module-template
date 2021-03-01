# noinspection PyCompatibility
from urllib.parse import quote_plus
from redis import Redis
import pymongo


class CommonLib:
    CONFIG = {
        'MONGODB_HOST': "mongo",
        "MONGODB_DB": "microservice",
        "MONGODB_USER": "root",
        "MONGODB_PW": "example",
        'REDIS_HOST': "redis",
        'REDIS_DB': 0,
        'TESTING': False,
    }
    redis = None
    db = None

    def establish_mongodb_connection(self):
        if self.db is None:
            uri = "mongodb://%s:%s@%s" % (
                quote_plus(self.CONFIG['MONGODB_USER']), quote_plus(self.CONFIG['MONGODB_PW']),
                quote_plus(self.CONFIG['MONGODB_HOST']))
            client = pymongo.MongoClient(uri)
            self.db = client[self.CONFIG['MONGODB_DB']]
        return self.db

    def establish_redis_connection(self):
        if self.redis is None:
            self.redis = Redis(host=self.CONFIG['REDIS_HOST'], db=self.CONFIG['REDIS_DB'], socket_connect_timeout=2, socket_timeout=2)
        return self.redis

