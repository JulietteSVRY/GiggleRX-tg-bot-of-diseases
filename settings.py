import json
import os

with open(os.environ.get("CONFIG_PATH"), "r") as f:
    config = json.load(f)

TOKEN = config["TOKEN"]
