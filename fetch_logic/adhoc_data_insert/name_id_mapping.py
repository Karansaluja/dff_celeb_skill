import logging

import pandas as pd
from constants import constants
from fetch_logic.mongo_db import mongo_db

logger = logging.getLogger(__name__)


def push_basic_celebs_data():
    print("reading file...")
    df = pd.read_csv(constants.CELEBS_FILE, sep="\t")
    number_of_celebs = df.shape[0]
    logger.info("Total number of rows {}".format(number_of_celebs))
    batch_size = 1000
    number_of_batches = number_of_celebs // batch_size
    start = 0
    logger.info("creating batches")
    for i in range(0, number_of_batches):
        subset = df.iloc[start:start + batch_size, :]
        logger.info("Created batch from {0} to {1}".format(start, start + batch_size))
        start = start + batch_size
        prepare_and_insert_celeb_data(subset, i)


def prepare_and_insert_celeb_data(rows: pd.DataFrame, batch_num: int):
    logger.info("processing batch {}".format(batch_num))
    records = []
    logger.info("number of row in batch {} : {}".format(batch_num, rows.shape[0]))
    count = 0
    for _, row in rows.iterrows():
        count += 1
        record = {"_id": row["nconst"], "name": row["primaryName"],
                  "birth_year": "" if len(row["birthYear"]) < 4 else row["birthYear"],
                  "death_year": "" if len(row["deathYear"]) < 4 else row["deathYear"],
                  "primary_profession": str(row["primaryProfession"]).split(","),
                  "known_for": str(row["knownForTitles"]).split(",")}
        records.append(record)
    mongo_db.insert_many("celeb", "basic_details", records)
    logger.info("Number of iterations for batch {0} : {1}".format(batch_num, count))
    logger.info("processed batch {}".format(batch_num))