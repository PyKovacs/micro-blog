import json


CONFIG = "config.json"

with open(CONFIG, "r") as config:
    conf_dict = json.load(config)

db_uri = conf_dict.get('mongodb_uri')
secret_key = conf_dict.get('secret_key')