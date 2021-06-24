import requests
import time
import json


# Метод для отправки запроса с токеном
def check_job(get_token, job_url):
    # Переменная в которой хранится полученный после первого запроса токен
    payload = {"token": get_token}
    # Делаем второй запрос до запуска джоба
    second_response = requests.get(job_url, params=payload)
    # Парсим ответ
    parsed_second_response = json.loads(second_response.text)

    # Проверяем какие поля нам вернулись в ответе
    get_status_job = parsed_second_response['status']
    if 'error' in parsed_second_response:
        get_error_job = parsed_second_response['error']
    else:
        get_error_job = "No error param in the JSON response"
    if 'result' in parsed_second_response:
        get_result_job = parsed_second_response['result']
    else:
        get_result_job = "No result param in the JSON response"

    # Выводим информацию пользователю
    print(get_error_job)
    print(get_status_job)
    print(get_result_job)


def main():
    # URL на который посылаем запрос
    job_url = "https://playground.learnqa.ru/ajax/api/longtime_job"
    # Делаем первый запрос, для создания джоба и получения токена
    first_response = requests.get(job_url)
    # Парсим ответ и вытаскивает токен и время выполнения джоба
    get_token = json.loads(first_response.text)['token']
    get_time = json.loads(first_response.text)['seconds']
    # Вызываем метод для отправки второго запроса и проверки статуса джоба
    check_job(get_token, job_url)
    print(f"Sleep the next {get_time} seconds...")
    # Ждем завершения джоба
    time.sleep(get_time+1)
    # Вызываем метод для отправки третьего запроса и проверки результата джоба
    check_job(get_token, job_url)


if __name__ == "__main__":
    main()