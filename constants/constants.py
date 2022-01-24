import re
MONGO_ADDRESS = "mongo_address"
CELEBS_FILE = "/Users/karansaluja/Downloads/name.basics.tsv"
CELEBS_DB = "celeb"
BASIC_CELEB_COLLECTION = "basic_details"
COLLECTION_STATS = "collstats"
TOP_ACTORS_FILE = "top_1000_actors.csv"
IMDB_URL = "http://www.imdb.com"
CELEB_PATH = "/name/"
BIO_COLLECTION = "bio"
MODEL_NAME = "deepset/roberta-base-squad2"
CACHE_LOCATION = "fetch_logic/hugging_face_cache"
HTML_CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')