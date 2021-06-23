import requests
import json

list_of_real_types = ["GET", "POST", "PUT", "DELETE"]
fake_method = "HEAD"

# Делаем запрос без параметра method
response_without_method = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type")

print("Checking request without method:")
print(response_without_method.text)

# Делаем запрос с заведомо некорректным методом
response_with_fake_method = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type",
                                          params={"method": f"{fake_method}"})
print("\nChecking request with fake method:")
print(response_with_fake_method.text)

# Делаем запрос с корректным значением метода
response_with_method = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type",
                                          params={"method": "GET"})
print("\nChecking request with real method:")
print(response_with_method.text)

# Пишем цикл для проверки всех возможных вариантов типа запросов и переданных методов
for item in range(len(list_of_real_types)):
    for element in range(len(list_of_real_types)):
        http_method = list_of_real_types[element].lower()
        header_method = list_of_real_types[item]
        if http_method in "get":
            response = requests.request(method=http_method, url="https://playground.learnqa.ru/ajax/api/compare_query_type",
                                        params={"method": f"{header_method}"})
        else:
            response = requests.request(method=http_method,
                                        url="https://playground.learnqa.ru/ajax/api/compare_query_type",
                                        data={"method": f"{header_method}"})
        print(f"\nType of request - {http_method} and method - {header_method}:")
        if http_method in header_method.lower():
            try:
                parsed_response = json.loads(response.text)
                print(parsed_response)
            except json.JSONDecodeError:
                print("Response not include any JSON object.")
        else:
            print(response.text)
