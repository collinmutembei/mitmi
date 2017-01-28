import unittest

import requests


class MITMITestCase(unittest.TestCase):

    def setUp(self):
        self.server_url = 'http://mitmi.herokuapp.com/api'
        self.test_username = "patientzer0"
        self.test_password = "YmlnZ2VzdGJlaGluZA"

    def test_get_method_not_allowed_on_signup(self):
        """ assert that GET request are not allowed on signup resource
        """
        signup_get = requests.get(
            "{0}/signup/".format(self.server_url),
            headers={"Accept": "application/json"},
        )
        self.assertEqual(signup_get.status_code, 405)

    def test_creating_new_user(self):
        """ assert that POST request on signup resource creates new user
        """
        signup_get = requests.post(
            "{0}/signup/".format(self.server_url),
            headers={"Accept": "application/json"},
            data={
                "username": self.test_username,
                "password": self.test_password
            }
        )
        self.assertEqual(signup_get.status_code, 200)

    def test_getting_token_for_existing_user(self):
        """ assert that signin for valid user gets token
        """
        signup_get = requests.post(
            "{0}/signin/".format(self.server_url),
            headers={"Accept": "application/json"},
            data={
                "username": self.test_username,
                "password": self.test_password
            }
        )
        self.assertEqual(signup_get.status_code, 200)

    def test_getting_token_for_non_existing_user(self):
        """ assert that signin for invalid user fails
        """
        signup_get = requests.post(
            "{0}/signin/".format(self.server_url),
            headers={"Accept": "application/json"},
            data={
                "username": "user",
                "password": "password"
            }
        )
        self.assertEqual(signup_get.status_code, 401)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
