import json

# Исходный текст для поиска текста сообщение
json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},\
                         {"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'

# Парсим переменную из текста в JSON
parsed_json_text = json.loads(json_text)
# Объявляем переменную для поиска первого ключа объекта JSON
json_key1 = "messages"
# Объявляем переменную для поиска второго ключа
json_key2 = "message"
# Номер сообщения, в котором ищем значение для вывода
message_number = 1

# Проверяем есть ли в переданной строке первый ключ
if json_key1 in parsed_json_text:
    # Проверяем есть в найденом значении второй ключ
    if json_key2 in parsed_json_text[json_key1][message_number]:
        # Выводим искомое значение
        print(parsed_json_text[json_key1][message_number][json_key2])
    else:
        print("Key json_key2 not found in json_text.")
else:
    print("Key json_key2 not found in json_text.")
