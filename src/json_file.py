import json

class JSONFile:
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            return []

    def write(self, data):
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)