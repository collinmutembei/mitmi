import unittest

from faker import Faker

from api.app import app, db
from api.config import config
from api.users.models import User


class MITMITestCase(unittest.TestCase):

    def setUp(self):
        app.config.from_object(config['testing'])
        self.client = app.test_client()

        self.fake = Faker()

        db.create_all()

        self.test_username = "patientzer0"
        self.test_password = "YmlnZ2VzdGJlaGluZA"

        test_user = User(
            username=self.test_username,
            password=self.test_password
        )
        db.session.add(test_user)
        db.session.commit()

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
                "username": self.fake.user_name(),
                "password": self.fake.password()
            }
        )
        self.assertEqual(signup_get.status_code, 201)

    def test_creating_new_user_with_username_of_existing_user(self):
        """ assert that POST request on signup resource with username
        matching an already existing user
        """
        signup_get = self.client.post(
            "/signup/",
            headers={"Accept": "application/json"},
            data={
                "username": "patientzer0",
                "password": self.fake.password()
            }
        )
        self.assertEqual(signup_get.status_code, 400)

    def test_creating_new_user_with_missing_field(self):
        """ assert that POST request on signup resource fails if required
        field is missing
        """
        signup_get = self.client.post(
            "/signup/",
            headers={"Accept": "application/json"},
            data={
                "username": self.fake.user_name(),
            }
        )
        self.assertEqual(signup_get.status_code, 400)

    def test_get_method_not_allowed_on_signin(self):
        """ assert that GET request are not allowed on signin resource
        """
        signup_get = self.client.get(
            "/signin/",
            headers={"Accept": "application/json"},
        )
        self.assertEqual(signup_get.status_code, 405)

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

    def test_getting_token_for_existing_user_with_wrong_password(self):
        """ assert that signin for valid user with wrong password
        """
        signup_get = self.client.post(
            "/signin/",
            headers={"Accept": "application/json"},
            data={
                "username": self.test_username,
                "password": self.fake.password()
            }
        )
        self.assertEqual(signup_get.status_code, 403)

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
