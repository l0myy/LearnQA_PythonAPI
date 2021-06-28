import requests

# Делаем GET запрос
response = requests.get("https://playground.learnqa.ru/api/long_redirect")
# Вычисляем длину response.history
length_of_response = len(response.history)
# Выводим количество редиректов
print(f"Number of redirects: {length_of_response}")

# Выводим все URL и Status_code всех редиректов.
for item in range(length_of_response):
    print(response.history[item].status_code)
    print(response.history[item].url)





