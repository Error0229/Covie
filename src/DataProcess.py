import json
import text2emotion as te
import cnsenti as cs

class DataProcess:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def process(data):
        print("data processing ...")
        return "over"
