import requests

class TestHomeWork2:
    def test_cookie_homework(self):

        response = requests.post("https://playground.learnqa.ru/api/homework_cookie")

        my_response = response.cookies.get_dict()

        assert 'HomeWork' in my_response, f"{my_response}"
        assert my_response['HomeWork'] == 'hw_value', f"{my_response['HomeWork']}"
