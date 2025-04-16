import yaml

data = ['RUB','USD',"MXN"]

# # Сохранение в файл `currency.yaml`
# with open("currency.yaml", "w") as file:
#     yaml.dump(data, file)

# Чтение файла `Test_file_1.yaml`
with open("currency.yaml", "r") as file:
    loaded_data = yaml.safe_load(file)
    print(loaded_data)