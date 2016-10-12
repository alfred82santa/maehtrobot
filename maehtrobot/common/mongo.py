from urllib.parse import urlencode

from dirty_loader.factories import BaseFactory
from motor.core import AgnosticClientBase, AgnosticDatabase, AgnosticCollection
from motor.motor_asyncio import AsyncIOMotorDatabase


class MongoDBFactory(BaseFactory):
    def __call__(self, hosts, username=None, password=None, database=None, **kwargs):

        def host_str(host):
            if isinstance(host, str):
                return host

            return ":".join([host['host'], host.get('port', 27017)])

        uri_str = 'mongodb://'

        if username:
            uri_str += ':'.join([username, password or ''])
            uri_str += '@'

        if isinstance(hosts, list):
            uri_str += ','.join([host_str(host) for host in hosts])
        else:
            uri_str += host_str(hosts)

        if database:
            uri_str += '/' + database

        if kwargs:
            uri_str += '?' + urlencode(kwargs)

        return super(MongoDBFactory, self).__call__(uri_str)


class MongoDatabaseFactory(BaseFactory):

    def __call__(self, connection, database, **kwargs):
        return connection[database]


class MongoCollectionFactory(BaseFactory):

    def __call__(self, database, collection, **kwargs):
        return database[collection]


def register_mongo_factories(loader):
    loader.register_factory(AgnosticClientBase, MongoDBFactory)
    loader.register_factory(AsyncIOMotorDatabase, MongoDatabaseFactory)
    loader.register_factory(AgnosticCollection, MongoCollectionFactory)
