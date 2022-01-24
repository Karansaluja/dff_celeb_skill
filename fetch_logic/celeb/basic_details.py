import logging
import re
from cachetools import TTLCache, cached
from fetch_logic.mongo_db import mongo_db
from constants import constants

logger = logging.getLogger(__name__)


@cached(cache=TTLCache(maxsize=20, ttl=10))
def get_basic_details(celeb_name):
    query = {"name": re.compile(celeb_name, re.IGNORECASE)}
    result = mongo_db.find_one_record(db_name=constants.CELEBS_DB,
                                      collection_name=constants.BASIC_CELEB_COLLECTION, query=query)
    return result
