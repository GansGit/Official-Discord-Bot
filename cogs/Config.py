import json

class Config():
    
    def get_config(name):
        with open("config.json", "r") as f:
            json_file = json.load(f)
        return json_file[name]