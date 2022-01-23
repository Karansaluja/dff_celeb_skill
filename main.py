# This is a sample Python script.
import asyncio
import logging
import copy
import re
import time
import os
from flow_logic import flow_graph, flow_handler
from fetch_logic.celeb import basic_details

from config import config
from df_engine.core import Actor
from fetch_logic.mongo_db import mongo_db
from fetch_logic.adhoc_data_insert import name_id_mapping

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
logger = logging.getLogger(__name__)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logfile = 'celeb_skill.log'
    if (os.path.isfile(logfile)):
        os.remove(logfile)
    logging.basicConfig(level=logging.INFO)
    file_handler = logging.FileHandler(logfile)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(pathname)s [%(process)d]: %(levelname)s:: %(message)s'))
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    """
     client = mongo_db.get_mongo_client()
    db = client["celebs"]
    collection = db["celeb_details"]
    celeb_record = {"name":"Leonardo DiCaprio","_id":"nm0000138"}
    _ = collection.insert_one(celeb_record)
    query = {"name": "Leonardo DiCaprio"}
    results = collection.find(query)
    for x in results:
        print(x)
    db_list = client.list_database_names()
    print(db_list)
    """
    #name_id_mapping.read_actors_file()

    cfg = config.Config()
    db = mongo_db.MongoDb(cfg, logger)
    """
    db.check_sample("celeb","basic_details")
    db.get_collection_size("celeb","basic_details")
    query = {"name": re.compile("Tom Cruise", re.IGNORECASE)}
    db.find_one_record("celeb","basic_details",query)
    """
    basic_celeb = basic_details.BasicDetails(db, logger)
    graph = flow_graph.FlowGraph(celeb_basics=basic_celeb, logger=logger)
    handler = flow_handler.FlowHandler(graph, logger=logger)
    #plot1= graph.plot
    #plot = copy.deepcopy(plot1)
    """
    setattr(cfg, '__deepcopy__', lambda self, _: self)
    setattr(db, '__deepcopy__', lambda self, _: self)
    setattr(basic_celeb, '__deepcopy__', lambda self, _: self)
    setattr(graph, '__deepcopy__', lambda self, _: self)

    actor = Actor(plot=graph.plot, start_label=("global", "start"))
    
    db.drop_collection("celeb","basic_details")
    celebDetails = name_id_mapping.BasicCelebDataInserter(logger,db)
    start_time = time.time()
    #name_id_mapping.push_basic_celebs_data()
    celebDetails.push_basic_celebs_data()
    duration = time.time() - start_time
    logger.info("took {} seconds to process data".format(duration))
    """
    ctx = {}
    while True:
        in_request = input("type your request: ")
        st_time = time.time()
        out_response, ctx = handler.turn_handler(in_request,ctx)
        print(f"{in_request:} -> {out_response}")
        total_time = time.time() - st_time
        print(f"exec time = {total_time:.3f}s")

