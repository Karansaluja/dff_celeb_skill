import logging
import re

from cachetools import TTLCache, cached
from fetch_logic.mongo_db import mongo_db
from constants import constants


class BasicDetails:
    def __init__(self, db: mongo_db.MongoDb, logger: logging.Logger):
        self.db = db
        self.logger = logger

    @cached(cache=TTLCache(maxsize=20, ttl=120))
    def get_basic_details(self, celeb_name):
        query = {"name": re.compile(celeb_name, re.IGNORECASE)}
        result = self.db.find_one_record(db_name=constants.CELEBS_DB,
                                         collection_name=constants.BASIC_CELEB_COLLECTION, query=query)
        return result
