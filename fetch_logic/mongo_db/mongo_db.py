import logging

import pymongo

from config import config
from constants import constants

host_address = config.get_config_value(constants.MONGO_ADDRESS)
mongo_client = pymongo.MongoClient(host_address)
logger = logging.getLogger(__name__)


def insert_one(db_name: str, collection_name: str, record):
    db = mongo_client[db_name]
    collection = db[collection_name]
    collection.insert_one(record)


def insert_many(db_name: str, collection_name: str, records):
    db = mongo_client[db_name]
    collection = db[collection_name]
    collection.insert_many(records)


def check_sample(db_name: str, collection_name: str):
    db = mongo_client[db_name]
    collection = db[collection_name]
    print(collection.find_one())


def get_collection_size(db_name: str, collection_name: str):
    db = mongo_client[db_name]
    print(db.command(constants.COLLECTION_STATS, collection_name))


def find_one_record(db_name: str, collection_name: str, query: dict):
    db = mongo_client[db_name]
    collection = db[collection_name]
    result = collection.find_one(query)
    return result


def find_records(db_name: str, collection_name: str, query: dict):
    db = mongo_client[db_name]
    collection = db[collection_name]
    results = collection.find(query)
    return results


def drop_collection(db_name: str, collection_name: str):
    db = mongo_client[db_name]
    collection = db[collection_name]
    collection.drop()
    logger.info("Dropped collection {0}".format(collection_name))