import json

class CareerPath():
    def __init__(self, json_file):
        self.graph = json.load(json_file)

        