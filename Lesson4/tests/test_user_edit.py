from Lesson3.lib.base_case import BaseCase
from Lesson3.lib.my_requests import MyRequests
from Lesson3.lib.assertions import Assertions
import allure


@allure.epic("Testing API methods to edit user information.")
class TestUserEdit(BaseCase):

    @allure.description("Testing API method to edit user recently created and changing .")
    def test_edit_just_created_user(self):
        # Registration
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # Login
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookies(response2, "auth_sid")
        token = self.get_headers(response2, "x-csrf-token")

        # Edit
        new_name = "Changed Name"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name})

        Assertions.assert_code_status(response3, 200)

        # Get
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )
        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit!"
        )

    @allure.description("Testing API method to get information without auth token.")
    def test_edit_user_without_auth_token(self):

        new_name = "Changed Name"

        response = MyRequests.put(f"/user/2",
                                   data={"firstName": new_name},
                                   headers={"x-csrf-token": "token"}
                                   )

        Assertions.assert_code_status(response, 400)

        assert response.text == "Auth token not supplied",  f"Unexpected response content {response.content}"

    @allure.description("Testing API method to get information with auth token from another user.")
    def test_edit_user_with_auth_another_user(self):
        # Register first user
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email1 = register_data['email']
        password1 = register_data['password']

        # Register second user
        register_data = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email2 = register_data['email']
        first_name2 = register_data['firstName']
        password2 = register_data['password']
        user_id2 = self.get_json_value(response2, "id")

        # Login as first user
        login_data1 = {
            'email': email1,
            'password': password1
        }

        response3 = MyRequests.post("/user/login", data=login_data1)

        auth_sid1 = self.get_cookies(response3, "auth_sid")
        token1 = self.get_headers(response3, "x-csrf-token")

        # Edit second user using token first's user.
        new_name = "Changed Name"

        response4 = MyRequests.put(f"/user/{user_id2}",
                                   headers={"x-csrf-token": token1},
                                   cookies={"auth_sid": auth_sid1},
                                   data={"firstName": new_name})

        Assertions.assert_code_status(response4, 200)

        # Login as second user
        login_data2 = {
            'email': email2,
            'password': password2
        }

        response5 = MyRequests.post("/user/login", data=login_data2)

        auth_sid2 = self.get_cookies(response5, "auth_sid")
        token2 = self.get_headers(response5, "x-csrf-token")

        response6 = MyRequests.get(f"/user/{user_id2}",
                                   headers={"x-csrf-token": token2},
                                   cookies={"auth_sid": auth_sid2})

        Assertions.assert_json_value_by_name(response6, "firstName", first_name2, f"Unexpected first name."
                                             f" Actual: {self.get_json_value(response6, 'firstName')},"
                                             f" Expected: {first_name2}")

    @allure.description("Testing API method to edit email authorized user without '@'.")
    def test_edit_user_email_without_at_symbol(self):
        # Register user
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # Login user
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookies(response2, "auth_sid")
        token = self.get_headers(response2, "x-csrf-token")

        # Edit email
        new_email = email.replace('@', '')

        response4 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"email": new_email})

        Assertions.assert_code_status(response4, 400)
        assert response4.text == "Invalid email format", f"Unexpected response content: {response4.content}"

    @allure.description("Testing API method to edit first name authorized user with length one character.")
    def test_edit_user_firstname_one_char_length(self):
        # Register user
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # Login user
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookies(response2, "auth_sid")
        token = self.get_headers(response2, "x-csrf-token")

        # Edit email
        new_firstname = 'l'

        response4 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_firstname})

        Assertions.assert_code_status(response4, 400)
        assert self.get_json_value(response4, 'error') == "Too short value for field firstName",\
                                                          f"Unexpected response content: {response4.text}"
