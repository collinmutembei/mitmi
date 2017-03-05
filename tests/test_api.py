import unittest
import json
from base64 import b64encode

from faker import Faker

from api.app import app, db
from api.config import config
from api.users.models import User
from api.events.models import Event


class MITMITestCase(unittest.TestCase):

    def setUp(self):
        app.config.from_object(config['testing'])
        self.client = app.test_client()

        self.fake = Faker()

        db.create_all()

        self.test_username = "patientzer0"
        self.test_password = "YmlnZ2VzdGJlaGluZA"

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # users

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
        signup_post = self.client.post(
            "/signup/",
            headers={"Accept": "application/json"},
            data={
                "username": self.fake.user_name(),
                "password": self.fake.password()
            }
        )
        self.assertEqual(signup_post.status_code, 201)

    def test_creating_new_user_with_username_of_existing_user(self):
        """ assert that POST request on signup resource with username
        matching an already existing user
        """
        test_user = User(
            username=self.test_username,
            password=self.test_password
        )
        db.session.add(test_user)
        db.session.commit()

        signup_post = self.client.post(
            "/signup/",
            headers={"Accept": "application/json"},
            data={
                "username": "patientzer0",
                "password": self.fake.password()
            }
        )
        self.assertEqual(signup_post.status_code, 400)

    def test_creating_new_user_with_missing_field(self):
        """ assert that POST request on signup resource fails if required
        field is missing
        """
        signup_post = self.client.post(
            "/signup/",
            headers={"Accept": "application/json"},
            data={
                "username": self.fake.user_name(),
            }
        )
        self.assertEqual(signup_post.status_code, 400)

    def test_get_method_not_allowed_on_signin(self):
        """ assert that GET request are not allowed on signin resource
        """
        signin_get = self.client.get(
            "/signin/",
            headers={"Accept": "application/json"},
        )
        self.assertEqual(signin_get.status_code, 405)

    def test_getting_token_for_existing_user(self):
        """ assert that signin for valid user gets token
        """
        test_user = User(
            username=self.test_username,
            password=self.test_password
        )
        db.session.add(test_user)
        db.session.commit()

        signin_post = self.client.post(
            "/signin/",
            headers={"Accept": "application/json"},
            data={
                "username": self.test_username,
                "password": self.test_password
            }
        )
        self.assertEqual(signin_post.status_code, 200)

    def test_getting_token_for_existing_user_with_wrong_password(self):
        """ assert that signin for valid user with wrong password
        """
        test_user = User(
            username=self.test_username,
            password=self.test_password
        )
        db.session.add(test_user)
        db.session.commit()

        signin_post = self.client.post(
            "/signin/",
            headers={"Accept": "application/json"},
            data={
                "username": self.test_username,
                "password": self.fake.password()
            }
        )
        self.assertEqual(signin_post.status_code, 403)

    def test_getting_token_for_non_existing_user(self):
        """ assert that signin for invalid user fails
        """
        signin_post = self.client.post(
            "/signin/",
            headers={"Accept": "application/json"},
            data={
                "username": "user",
                "password": "password"
            }
        )
        self.assertEqual(signin_post.status_code, 401)

    # events

    def test_logged_in_user_can_create_event(self):
        """ assert that users who have been authenticated can
        create event
        """
        test_user = User(
            username=self.test_username,
            password=self.test_password
        )
        db.session.add(test_user)
        db.session.commit()

        signin_test_user = self.client.post(
            'signin/',
            data={
                "username": self.test_username,
                "password": self.test_password
            }
        )
        signin = json.loads(signin_test_user.data)
        user_token = signin["token"]

        event = self.client.post(
            "/event/",
            headers={
                "Authorization": "Bearer {0}".format(user_token),
                "Accept": "application/json"
            },
            data={
                "name": "dunda",
                "venue": "kejani"
            }
        )
        self.assertEqual(event.status_code, 201)

    def test_not_logged_in_user_cannot_create_event(self):
        """ assert that users who have not been authenticated cannot
        create an event
        """
        event = self.client.post(
            "/event/",
            headers={"Accept": "application/json"},
            data={
                "name": "dunda",
                "venue": "kejani"
            }
        )
        self.assertEqual(event.status_code, 401)

    def test_logged_in_user_can_view_specific_event(self):
        """ assert that users who have been authenticated can
        view all events
        """
        test_user = User(
            username=self.test_username,
            password=self.test_password
        )
        db.session.add(test_user)
        db.session.commit()

        signin_test_user = self.client.post(
            'signin/',
            data={
                "username": self.test_username,
                "password": self.test_password
            }
        )
        signin = json.loads(signin_test_user.data)
        user_token = signin["token"]

        event = self.client.post(
            "/event/",
            headers={
                "Authorization": "Bearer {0}".format(user_token),
                "Accept": "application/json"
            },
            data={
                "name": "party",
                "venue": "house"
            }
        )

        existing_event = Event.query.filter_by(
            name="party"
        ).first()
        events = self.client.get(
            "/event/{0}/".format(existing_event.id),
            headers={
                "Authorization": "Bearer {0}".format(user_token)
            }
        )
        self.assertEqual(events.status_code, 200)

    def test_logged_in_user_can_view_event(self):
        """ assert that users who have been authenticated can
        view all events
        """
        test_user = User(
            username=self.test_username,
            password=self.test_password
        )
        db.session.add(test_user)
        db.session.commit()

        signin_test_user = self.client.post(
            'signin/',
            data={
                "username": self.test_username,
                "password": self.test_password
            }
        )
        signin = json.loads(signin_test_user.data)
        user_token = signin["token"]

        events = self.client.get(
            "/event/",
            headers={
                "Authorization": "Bearer {0}".format(user_token)
            }
        )
        self.assertEqual(events.status_code, 200)

    def test_not_logged_in_user_cannot_view_events(self):
        """ assert that users who have not been authenticated cannot
        see all event
        """
        events = self.client.get(
            "/event/"
        )
        self.assertEqual(events.status_code, 401)

    def test_logged_in_user_update_an_event_they_created(self):
        """ assert that users who have been authenticated can
        update an event they created
        """
        test_user = User(
            username=self.test_username,
            password=self.test_password
        )
        db.session.add(test_user)
        db.session.commit()

        signin_test_user = self.client.post(
            'signin/',
            data={
                "username": self.test_username,
                "password": self.test_password
            }
        )
        signin = json.loads(signin_test_user.data)
        user_token = signin["token"]

        event = self.client.post(
            "/event/",
            headers={
                "Authorization": "Bearer {0}".format(user_token),
                "Accept": "application/json"
            },
            data={
                "name": "party",
                "venue": "house"
            }
        )

        existing_event = Event.query.filter_by(
            name="party"
        ).first()
        updated_event = self.client.put(
            "/event/{0}/".format(existing_event.id),
            headers={
                "Authorization": "Bearer {0}".format(user_token)
            },
            data={
                "venue": "kejani"
            }
        )
        self.assertEqual(updated_event.status_code, 200)

    def test_logged_in_user_cannot_update_an_event_they_did_not_create(self):
        """ assert that users who have been authenticated cannot
        update an event created by someone else
        """
        other_user = User(
            username=self.test_username,
            password=self.test_password
        )
        db.session.add(other_user)
        db.session.commit()

        signin_other_user = self.client.post(
            'signin/',
            data={
                "username": self.test_username,
                "password": self.test_password
            }
        )
        signin = json.loads(signin_other_user.data)
        user_token = signin["token"]

        event = self.client.post(
            "/event/",
            headers={
                "Authorization": "Bearer {0}".format(user_token),
                "Accept": "application/json"
            },
            data={
                "name": "party",
                "venue": "house"
            }
        )

        test_user = User(
            username="test_user",
            password="test_password"
        )
        db.session.add(test_user)
        db.session.commit()

        signin_test_user = self.client.post(
            'signin/',
            data={
                "username": "test_user",
                "password": "test_password"
            }
        )
        signin = json.loads(signin_test_user.data)
        user_token = signin["token"]

        existing_event = Event.query.filter_by(
            name="party"
        ).first()
        updated_event = self.client.put(
            "/event/{0}/".format(existing_event.id),
            headers={
                "Authorization": "Bearer {0}".format(user_token)
            },
            data={
                "venue": "kejani"
            }
        )
        self.assertEqual(updated_event.status_code, 404)

    def test_not_logged_in_user_cannot_update_an_event(self):
        """ assert that users who have not been authenticated cannot
        update events
        """
        test_user = User(
            username=self.test_username,
            password=self.test_password
        )
        db.session.add(test_user)
        db.session.commit()

        signin_test_user = self.client.post(
            'signin/',
            data={
                "username": self.test_username,
                "password": self.test_password
            }
        )
        signin = json.loads(signin_test_user.data)
        user_token = signin["token"]

        event = self.client.post(
            "/event/",
            headers={
                "Authorization": "Bearer {0}".format(user_token),
                "Accept": "application/json"
            },
            data={
                "name": "party",
                "venue": "house"
            }
        )

        existing_event = Event.query.filter_by(
            name="party"
        ).first()
        updated_event = self.client.put(
            "/event/{0}/".format(existing_event.id),
            data={
                "venue": "kejani"
            }
        )
        self.assertEqual(updated_event.status_code, 401)

if __name__ == '__main__':
    unittest.main()
