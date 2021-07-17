from Lesson3.lib.base_case import BaseCase
from Lesson3.lib.assertions import Assertions
from Lesson3.lib.my_requests import MyRequests
import allure


@allure.epic("Testing methods to get user data.")
class TestUserGet(BaseCase):

    @allure.description("Testing methods to get details not auth users.")
    def test_get_user_details_not_auth(self):
        with allure.step("Get information about user with ID = 2."):
            response = MyRequests.get("/user/2")
        with allure.step("Checking keys from the response."):
            Assertions.assert_json_has_key(response, 'username')
            Assertions.assert_json_has_not_key(response, 'email')
            Assertions.assert_json_has_not_key(response, 'firstName')
            Assertions.assert_json_has_not_key(response, 'lastName')

    @allure.description("Testing methods to get details auth user.")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        with allure.step("Login user"):
            response1 = MyRequests.post("/user/login", data=data)

            auth_sid = self.get_cookies(response1, 'auth_sid')
            token = self.get_headers(response1, "x-csrf-token")
            user_id_from_auth_method = self.get_json_value(response1, "user_id")

        with allure.step(f"Get information user with ID: {user_id_from_auth_method}."):
            response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid}
                                     )

        expected_fields = ["username", "email", "firstName", "lastName"]

        with allure.step("Checking keys from the response."):
            Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.description("Testing methods to get details user with token another auth user.")
    def test_get_user_details_auth_as_another_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        with allure.step("Login first user."):
            response1 = MyRequests.post("/user/login", data=data)

            auth_sid = self.get_cookies(response1, 'auth_sid')
            token = self.get_headers(response1, "x-csrf-token")

        with allure.step("Get info with user ID: 2215."):
            response2 = MyRequests.get(f"/user/2215",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid}
                                       )

        with allure.step("Checking keys from the response."):
            Assertions.assert_json_has_key(response2, 'username')
            Assertions.assert_json_has_not_key(response2, 'email')
            Assertions.assert_json_has_not_key(response2, 'firstName')
            Assertions.assert_json_has_not_key(response2, 'lastName')
