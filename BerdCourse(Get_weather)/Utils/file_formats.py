import yaml
import pandas as pd
import json


class FileFormats:

    def __init__(self):
        self.data = []

    # ФОРМАТ YAML

    def write_yaml(self, data, name_file):
        with open(name_file, "w", encoding="utf-8") as file:
            yaml.dump(data, file, allow_unicode=True, default_flow_style=False)

    def read_yaml(self, name_file):
        with open(name_file, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    # ФОРМАТ JSON

    def write_json(self, data, name_file):
        with open(name_file, "w") as file:
            json.dump(data, file, indent=4)

    def read_json(self, name_file):
        with open(name_file, "r", encoding="utf-8") as file:
            return json.load(file)

    # ФОРМАТ CSV

    def write_csv(self, data, name_file):
        df = pd.DataFrame(data)
        df.to_csv(name_file, index=False, encoding="utf-8")

    def read_csv(self, name_file):
        df = pd.read_csv(name_file)
        data = df.to_dict(orient="records")
        return data

# file_1 = FileFormats()
# data = ['Москва', 'Бишкек', 'Ташкент', 'Анталия']
# f1 = file_1.write_yaml(data, 'cityes.yaml')
# print(f1)
# print(type(f1))
# file_1.write_json(f1, 'file5.json')

