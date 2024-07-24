import json

from modules.exception import CredsException


class Config:
    def __init__(self, path):
        self.path = path
        self.data = None


    def prepare_data(self):
        self.upload_data()
        self.check_data()

        return self.data


    def upload_data(self):
        with open(self.path) as file:
            self.data = json.load(file)


    def check_data(self):
        for key, value in self.data.items():
            if key in ("username", "password") and value == "":
                raise CredsException()
