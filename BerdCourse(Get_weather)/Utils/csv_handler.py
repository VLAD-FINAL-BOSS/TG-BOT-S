import pandas as pd
import os
from datetime import datetime


class CSVHandler:
    def save_csv(self, data, folder="saved_csv"):
        # Создаем папку, если её нет
        os.makedirs(folder, exist_ok=True)

        # Формируем имя файла с текущей датой и временем
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
        filepath = os.path.join(folder, filename)

        df = pd.DataFrame(data)

        # Сохраняем DataFrame в CSV
        df.to_csv(filepath, index=False)
        print(f"Файл сохранён: {filepath}")

    def read_csv(self, name_file):
        df = pd.read_csv(name_file)
        data = df.to_dict(orient="records")
        return data

# # # Пример использования
# handler = CSVHandler()
# # df = pd.DataFrame({"Name": ["Alice", "Bob"], "Age": [25, 30]})
# # handler.save_csv(df)
#
# data = ({"Name": ["Alice", "Bob"], "Age": [25, 30]})
# handler.save_csv(data)