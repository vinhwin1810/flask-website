import unittest
from flask import Flask
from flask_testing import TestCase
from website import views, db, models, create_app
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

class TestViews(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

        with app.app_context():
            db.create_all()
            user = models.User(email='test_user', password=generate_password_hash('test_password'))
            db.session.add(user)
            db.session.commit()

        return app

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_route(self):
        with self.client:
            # Login the user
            response = self.client.post('/login', data=dict(email='test_user', password='test_password'))
            self.assertEqual(response.status_code, 302)  # Expecting redirect

            # Follow the redirect
            response = self.client.get(response.headers['Location'])
            self.assertEqual(response.status_code, 200)

            # Send a POST request to add a note
            response = self.client.post('/', data=dict(note='Test note'))
            self.assertEqual(response.status_code, 200)
            self.assert_message_flashed('Note added!', 'success')

            # Send a POST request with an empty note
            response = self.client.post('/', data=dict(note=''))
            self.assertEqual(response.status_code, 200)
            self.assert_message_flashed('Note is too short!', 'error')

            # Send a GET request to render the home page
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            # Add more assertions to validate the response as needed


    def test_delete_note_route(self):
        with self.client:
            # Login the user
            response = self.client.post('/login', data=dict(email='test_user', password='test_password'))
            self.assertEqual(response.status_code, 302)  # Expecting redirect

            # Follow the redirect
            response = self.client.get(response.headers['Location'])
            self.assertEqual(response.status_code, 200)

            # Send a POST request to delete a note
            response = self.client.post('/delete-note', json={'noteId': 1})
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
