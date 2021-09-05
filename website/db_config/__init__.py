import json
import os


class CharLimits:
    with open("./website/db_config/char_limits.json", "r") as f:
        data = json.load(f)
    user = data["user"]
    post = data["post"]
    