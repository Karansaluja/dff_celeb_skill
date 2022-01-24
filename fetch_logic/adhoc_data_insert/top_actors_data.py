import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from fetch_logic.mongo_db import mongo_db
from constants import constants
import logging

logger = logging.getLogger(__name__)


def store_top_celebs_bio():
    mongo_db.drop_collection(constants.CELEBS_DB, constants.BIO_COLLECTION)
    df = pd.read_csv(constants.TOP_ACTORS_FILE, encoding="ISO-8859-1")
    records = []
    for _, row in df.iterrows():
        celeb_id = row['Const']
        record = get_celeb_record(celeb_id, row['Name'])
        if record is None:
            continue
        records.append(record)
        logger.info("got bio for {}".format(row['Name']))
    mongo_db.insert_many(constants.CELEBS_DB, constants.BIO_COLLECTION, records)
    logger.info("Successfully inserted to celeb bio to mongo db")


def clean_html(raw_html):
    return re.sub(constants.HTML_CLEANR, '', raw_html)


def get_celeb_data(celeb_id: str, celeb_name: str) -> str:
    record = get_celeb_record(celeb_id, celeb_name)
    if record is None:
        return "Sorry, I couldn't find anything about {}".format(celeb_name)
    mongo_db.insert_one(constants.CELEBS_DB, constants.BIO_COLLECTION, record)
    return record["bio"]


def get_celeb_record(celeb_id: str, celeb_name: str):
    bio_url = constants.IMDB_URL + constants.CELEB_PATH + celeb_id + "/bio"
    page = requests.get(bio_url)
    if page.status_code != 200:
        logger.error("No data found for celeb:{0} on IMDB".format("celeb_name"))
        return None
    soup = BeautifulSoup(page.content, "html.parser")
    ele = soup.find("div", {"class": "soda odd"})
    op = ele.find("p")
    bio = clean_html(op.text)
    record = {"_id": celeb_id, "name": celeb_name, "bio": bio}
    return record
