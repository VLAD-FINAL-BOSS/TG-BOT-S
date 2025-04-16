from Utils.get_weather_info import GetWeather
from Utils.file_formats import FileFormats
from Utils.csv_handler import CSVHandler
import pandas as pd

# Читаем ямл файл ситиес
fl = FileFormats()
data_list = fl.read_yaml('cityes.yaml')

my_dict = []

gw = GetWeather()
for elem in data_list:
    my_dict.append(gw.get_weather_info(elem))


handler = CSVHandler()
handler.save_csv(my_dict)

# fl_2 = FileFormats()
# fl_2.write_csv(my_dict, "prognoz.csv")
#
# fl_3 = FileFormats()
# qwer = fl_3.read_csv("prognoz.csv")
# print(qwer)





