import allure
from Lesson3.lib.base_case import BaseCase
from Lesson3.lib.assertions import Assertions
from Lesson3.lib.my_requests import MyRequests


@allure.epic("Testing API methods to delete users.")
class TestUserDelete(BaseCase):

    @allure.description("Testing API method which delete user with user_id = 2.")
    def test_delete_user_with_known_id(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        # Login
        with allure.step("Login user."):
            response1 = MyRequests.post("/user/login", data=data)

            auth_sid = self.get_cookies(response1, "auth_sid")
            token = self.get_headers(response1, "x-csrf-token")
            user_id = self.get_json_value(response1, 'user_id')

        # Delete
        with allure.step("Delete user."):
            response2 = MyRequests.delete(f"/user/{user_id}",
                                          headers={"x-csrf-token": token},
                                          cookies={"auth_sid": auth_sid},
                                          data=data)

            Assertions.assert_code_status(response2, 400)

        with allure.step("Assertion response."):
            assert response2.text == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",\
                                     f"Unexpected response content: {response2.content}"

    @allure.description("Testing API method to delete user with auth token and after check info.")
    def test_delete_user_and_check_info(self):
        # Registration
        with allure.step("Registration user."):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data['email']
            password = register_data['password']
            user_id = self.get_json_value(response1, "id")

        # Login
        with allure.step("Login user."):
            login_data = {
                'email': email,
                'password': password
            }

            response2 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookies(response2, "auth_sid")
            token = self.get_headers(response2, "x-csrf-token")

        # Delete
        with allure.step("Delete user."):
            response3 = MyRequests.delete(f"/user/{user_id}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid},
                                       data=login_data)

        with allure.step("Checking status code from the response."):
            Assertions.assert_code_status(response3, 200)

        # Get
        with allure.step("Get user."):
            response4 = MyRequests.get(f"/user/{user_id}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid}
                                       )

        with allure.step("Checking text from the response."):
            assert response4.text == 'User not found', f"Unexpected response content: {response4.content}."

    @allure.description("Testing API method to delete user using auth token another user.")
    def test_delete_user_with_token_another_user(self):
        # Register first user
        with allure.step("Register first user."):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post("/user/", data=register_data)

        with allure.step("Checking status_code and ID first user from the response."):
            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email1 = register_data['email']
            password1 = register_data['password']

        # Register second user
        with allure.step("Register second user."):
            register_data = self.prepare_registration_data()
            response2 = MyRequests.post("/user/", data=register_data)

        with allure.step("Checking status_code and ID second user from the response."):
            Assertions.assert_code_status(response2, 200)
            Assertions.assert_json_has_key(response2, "id")

            user_id2 = self.get_json_value(response2, "id")

        # Login as first user
        with allure.step("Login as first user."):
            login_data1 = {
                'email': email1,
                'password': password1
            }

            response3 = MyRequests.post("/user/login", data=login_data1)

            auth_sid1 = self.get_cookies(response3, "auth_sid")
            token1 = self.get_headers(response3, "x-csrf-token")

        # Delete second user using token first's user.
        with allure.step("Delete second user using token first's user."):
            response4 = MyRequests.delete(f"/user/{user_id2}",
                                       headers={"x-csrf-token": token1},
                                       cookies={"auth_sid": auth_sid1},
                                       data=login_data1)

        with allure.step("Checking status_code from the response."):
            Assertions.assert_code_status(response4, 200)

        # Get second user info
        with allure.step("Get second user info."):
            response5 = MyRequests.get(f"/user/{user_id2}")

        with allure.step("Checking status_code and username from the response."):
            Assertions.assert_code_status(response5, 200)
            Assertions.assert_json_has_key(response5, "username")
