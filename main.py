# This is a sample Python script.
from flow_logic import flow_handler,flow_graph
from fetch_logic.adhoc_data_insert import top_actors_data
import logging
import os
import time
from fetch_logic.mongo_db import mongo_db
from fetch_logic.hugging_face import hugging_face
from constants import constants
import re

logger = logging.getLogger(__name__)
if __name__ == '__main__':
    logfile = 'celeb_skill.log'
    if os.path.isfile(logfile):
        os.remove(logfile)
    logging.basicConfig(level=logging.INFO)
    file_handler = logging.FileHandler(logfile)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(pathname)s [%(process)d]: %(levelname)s:: %(message)s'))
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    ctx = {}
    while True:
        in_request = input("type your request: ")
        st_time = time.time()
        out_response, ctx = flow_handler.turn_handler(in_request, ctx, flow_graph.actor)
        print(f"{in_request:} -> {out_response}")
        total_time = time.time() - st_time
        print(f"exec time = {total_time:.3f}s")

    """
    query = {"name": re.compile("Tom Cruise", re.IGNORECASE)}
    record = mongo_db.find_one_record(constants.CELEBS_DB, constants.BIO_COLLECTION, query)
    print(hugging_face.get_ml_answer("when was he born", record["bio"]))
    #result = re.search(r".* (his|her|.+) .*", "when was tom cruise born", re.IGNORECASE)
    #print(result.groups())
    """


