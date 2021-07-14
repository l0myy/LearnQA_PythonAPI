from Lesson3.lib.base_case import BaseCase
from Lesson3.lib.assertions import Assertions
from Lesson3.lib.my_requests import MyRequests
import allure
import pytest
import random
import string


@allure.epic("Registration cases")
class TestUserRegister(BaseCase):

    @allure.description("Testing registration with random registration data")
    def test_create_user_successfully(self):

        data = self.prepare_registration_data()

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("Testing registration with existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'

        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists",\
            f"Unexpected response content {response.content}"

    @allure.description("Testing registration without '@' in the email. ")
    def test_create_user_with_incorrect_email(self):
        email = 'vinkotovexample.com'

        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format",\
            f"Unexpected response content {response.content}"

    missing_param = ['email', 'lastName', 'firstName', 'username', 'password']

    @allure.description("Testing registration without any field.")
    @pytest.mark.parametrize('missing_param', missing_param)
    def test_create_user_without_any_field(self, missing_param):

        data = self.prepare_registration_data()

        del data[missing_param]

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == f"The following required params are missed: {missing_param}",\
            f"Unexpected response content {response.content}"

    @allure.description("Testing registration with username length only 1 character.")
    def test_create_user_with_one_symbol(self):

        data = self.prepare_registration_data()

        data['firstName'] = 'l'

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == "The value of 'firstName' field is too short", \
            f"Unexpected response content {response.content}"

    @allure.description("Testing registration with username length more then 250 symbols.")
    def test_create_user_with_long_firstname(self):

        first_long_name = ''.join(random.choice(string.ascii_lowercase) for i in range(random.randint(251, 255)))

        data = self.prepare_registration_data()

        data['firstName'] = first_long_name

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == "The value of 'firstName' field is too long", \
            f"Unexpected response content {response.content}"

