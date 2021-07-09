import requests
import pytest


class TestFirstAPI:
    names = [
        ("Anatolii"),
        ("Evgeniya"),
        ("")
    ]

    @pytest.mark.parametrize('name', names)
    def test_hello_call(self, name):
        url = "https://playground.learnqa.ru/api/hello"
        print(name)
        data = {'name': name}

        response = requests.get(url, params=data)

        assert response.status_code == 200, f"Wrong response code."

        response_dict = response.json()
        assert "answer" in response_dict, f"There is no field 'answer' in the response"
        
        if len(name) == 0:
            expected_response_text = "Hello, someone"
        else:
            expected_response_text = f"Hello, {name}"

        actual_response_text = response_dict['answer']
        assert expected_response_text == actual_response_text, f"Actual response is not correct."
