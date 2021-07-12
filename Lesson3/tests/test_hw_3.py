import requests


class TestHomeWork3:
    def test_header_homework(self):

        response = requests.post("https://playground.learnqa.ru/api/homework_header")

        my_response = response.headers

        assert 'x-secret-homework-header' in my_response, f"{my_response}"
        assert my_response['x-secret-homework-header'] == "Some secret value", f"{my_response['x-secret-homework-header']}"
