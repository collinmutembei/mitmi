import unittest

from api.app import app, db


class MITMITestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

        self.test_username = "patientzer0"
        self.test_password = "YmlnZ2VzdGJlaGluZA"

        db.create_all()

    def test_get_method_not_allowed_on_signup(self):
        """ assert that GET request are not allowed on signup resource
        """
        signup_get = self.client.get(
            "/signup/",
            headers={"Accept": "application/json"},
        )
        self.assertEqual(signup_get.status_code, 405)

    def test_creating_new_user(self):
        """ assert that POST request on signup resource creates new user
        """
        signup_get = self.client.post(
            "/signup/",
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
        signup_get = self.client.post(
            "/signin/",
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
        signup_get = self.client.post(
            "/signin/",
            headers={"Accept": "application/json"},
            data={
                "username": "user",
                "password": "password"
            }
        )
        self.assertEqual(signup_get.status_code, 401)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
