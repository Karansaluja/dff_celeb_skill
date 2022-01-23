import logging

import pymongo

from config import config
from constants import constants
from custom_exceptions import exceptions


class MongoDb:
    def __init__(self, cfg: config.Config, logger: logging.Logger):
        self.config = cfg
        self.logger = logger
        try:
            host_address = self.config.get_config_value(constants.MONGO_ADDRESS)
        except exceptions.ConfigNotFoundException as exp:
            self.logger.error("failed to get mongo address")
            raise exp
        self.client = pymongo.MongoClient(host_address)
        self.logger.info("successfully connected to mongo server",exc_info=self.client.server_info())

    def insert_one(self, db_name: str, collection_name: str, record):
        db = self.client[db_name]
        collection = db[collection_name]
        collection.insert_one(record)

    def insert_many(self, db_name: str, collection_name: str, records):
        db = self.client[db_name]
        collection = db[collection_name]
        collection.insert_many(records)

    def check_sample(self, db_name: str, collection_name: str):
        db = self.client[db_name]
        collection = db[collection_name]
        print(collection.find_one())

    def get_collection_size(self, db_name: str, collection_name: str):
        db = self.client[db_name]
        print(db.command("collstats",collection_name))

    def find_one_record(self, db_name: str, collection_name: str, query: dict):
        db = self.client[db_name]
        collection = db[collection_name]
        result = collection.find_one(query)
        return result

    def find_records(self, db_name: str, collection_name: str, query: dict):
        db = self.client[db_name]
        collection = db[collection_name]
        results = collection.find(query)
        for x in results:
            print(x)

    def drop_collection(self, db_name: str, collection_name: str):
        db = self.client[db_name]
        collection = db[collection_name]
        collection.drop()
        self.logger.info("Dropped collection {0}".format(collection_name))

