import logging

import pandas as pd
from constants import constants
from fetch_logic.mongo_db import mongo_db


# Dataset was downloaded from https://datasets.imdbws.com/ -> title.ratings.tsv.gz
class BasicCelebDataInserter:
    def __init__(self, logger: logging.Logger, db: mongo_db.MongoDb):
        self.logger = logger #logging.getLogger(__name__)
        self.db = db
        #logging.basicConfig(level=logging.INFO)

    def push_basic_celebs_data(self):
        print("reading file...")
        df = pd.read_csv(constants.CELEBS_FILE, sep="\t")
        number_of_celebs = df.shape[0]
        self.logger.info("Total number of rows {}".format(number_of_celebs))
        batch_size = 1000
        number_of_batches = number_of_celebs // batch_size
        start = 0
        self.logger.info("creating batches")
        for i in range(0, number_of_batches):
            subset = df.iloc[start:start + batch_size, :]
            self.logger.info("Created batch from {0} to {1}".format(start, start + batch_size))
            start = start + batch_size
            self.prepare_and_insert_celeb_data(subset, i)

    def prepare_and_insert_celeb_data(self,rows: pd.DataFrame, batch_num: int):
        self.logger.info("processing batch {}".format(batch_num))
        records = []
        self.logger.info("number of row in batch {} : {}".format(batch_num,rows.shape[0]))
        count = 0
        for _, row in rows.iterrows():
            count +=1
            record = {"_id": row["nconst"], "name": row["primaryName"],
                      "birth_year": "" if len(row["birthYear"]) < 4 else row["birthYear"],
                      "death_year": "" if len(row["deathYear"]) < 4 else row["deathYear"],
                      "primary_profession": str(row["primaryProfession"]).split(","),
                      "known_for": str(row["knownForTitles"]).split(",")}
            records.append(record)
        self.db.insert_many("celeb","basic_details", records)
        self.logger.info("Number of iterations for batch {0} : {1}".format(batch_num, count))
        self.logger.info("processed batch {}".format(batch_num))