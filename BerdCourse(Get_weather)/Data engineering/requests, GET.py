
#
# URL = f"https://www.googleapis.com/oauth2/v3/userinfo"
#
# r = requests.get(url=URL)
#
# result = r.json()
#
# print(result)
# print(type(result))

import requests
# GET запрос

api_key = 'aec40cdd504ca4b4d150a173acf1f237'
date = '2025-03-05'  # Дата должна быть строкой

URL = f"http://data.fixer.io/api/{date}"

# Параметры запроса
params = {
    "access_key": api_key,
    "base": "EUR",  # Базовая валюта
    "symbols": "USD"  # Целевые валюты
}

# Отправка GET-запроса
r = requests.get(URL, params=params)

# Получение JSON-ответа
result = r.json()
print(result)

print("HTTP статус:", r.status_code)
print("Ответ сервера:", result)


# POST запросы

# # Set up the URL
# url = 'http://45.135.233.242:8001/to_insert'
#
# # Set up the headers
# # В headers передаются дополнительные параметры HTTP-запроса,
# # которые могут требоваться серверу для корректной обработки запроса.
# headers = {
#     'Content-Type': 'application/json',
#     'Authorization': 'Bearer your_token'
# }
#
# # Set up the request body
# payload = {
#     'symbol': '125'
# }
# json_payload = json.dumps(payload)
# print(payload)
#
# # Make the POST request
# response = requests.post(url=url, params=payload)
# print(response)
# # Check the response
# if response.status_code == 200:
#     print('Request successful!')
#     print(response.json())
# else:
#     print('Request failed!')
#     print(response.text)

















