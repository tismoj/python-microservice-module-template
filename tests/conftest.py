# noinspection PyCompatibility
from urllib.parse import quote_plus
from redis import Redis
from api import api
import pymongo
import pytest

CONFIG = {
    'MONGODB_HOST': "localhost",
    "MONGODB_DB": "microservice_test",
    "MONGODB_USER": "root",
    "MONGODB_PW": "example",
    'REDIS_HOST': "localhost",
    'REDIS_DB': 1,
    'TESTING': True,
}


@pytest.fixture(scope='module')
def api_client():
    client = api.app.test_client()
    # Enable the TESTING flag to disable the error catching during request handling
    # so that you get better error reports when performing test requests against the application.
    api.app.config['TESTING'] = True
    api.CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost"}

    # Establish an application context before running the tests.
    app_context = api.app.app_context()
    app_context.push()

    yield client

    app_context.pop()


@pytest.fixture(scope='function')
def db_client():
    uri = "mongodb://%s:%s@%s" % (
        quote_plus(CONFIG['MONGODB_USER']), quote_plus(CONFIG['MONGODB_PW']), quote_plus(CONFIG['MONGODB_HOST']))
    client = pymongo.MongoClient(uri)
    db = client[CONFIG['MONGODB_DB']]
    print()
    db.globals.drop()
    print('Dropped globals db collection')
    db.received_events.drop()
    print('Dropped received_events db collection')
    return db


@pytest.fixture(scope='function')
def redis_client():
    redis = Redis(host=CONFIG['REDIS_HOST'], db=CONFIG['REDIS_DB'], socket_connect_timeout=2, socket_timeout=2)
    print()
    return redis

