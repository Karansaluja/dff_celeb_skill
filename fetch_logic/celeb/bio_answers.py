import logging
import re
from cachetools import TTLCache, cached
from df_engine.core import Context
from fetch_logic.mongo_db import mongo_db
from constants import constants
from fetch_logic.hugging_face import hugging_face
from fetch_logic.adhoc_data_insert import top_actors_data

logger = logging.getLogger(__name__)


@cached(cache=TTLCache(maxsize=20, ttl=60))
def get_celeb_bio_by_name(name: str):
    query = {"name": re.compile(name, re.IGNORECASE)}
    record = mongo_db.find_one_record(constants.CELEBS_DB, constants.BIO_COLLECTION, query)
    return record


@cached(cache=TTLCache(maxsize=20, ttl=60))
def get_celeb_bio_by_id(celeb_id: str, name: str):
    query = {"_id": celeb_id}
    record = mongo_db.find_one_record(constants.CELEBS_DB, constants.BIO_COLLECTION, query)
    if record is None:
        logger.info("Didn't find data for {} in database. Checking the web...".format(name))
        return top_actors_data.get_celeb_data(celeb_id,name)
    return record["bio"]


def get_celeb_answer(ctx: Context, query: str) -> str:
    if ctx.misc.get("id") is not None:
        bio = get_celeb_bio_by_id(ctx.misc.get("id"), ctx.misc.get("name"))
        return hugging_face.get_ml_answer(query, bio)
    if ctx.misc.get("name") is not None:
        record = get_celeb_bio_by_name(ctx.misc.get("name"))
        ctx.misc["id"] = record["_id"]
        bio = record["bio"]
        return hugging_face.get_ml_answer(query, bio)
    return "Sorry, I don't have answer for that."
