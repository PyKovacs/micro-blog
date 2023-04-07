import json


CONFIG = "config.json"

with open(CONFIG, "r") as config:
    conf_dict = json.load(config)

db_uri: str = conf_dict.get('mongodb_uri')
secret_key: str = conf_dict.get('secret_key')