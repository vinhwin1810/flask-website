import unittest
from flask import Flask
from flask_testing import TestCase
from website import create_app, db
from website.models import User
from werkzeug.security import generate_password_hash
from flask import url_for
from flask_login import current_user

class TestAuthViews(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login_success(self):
        # Create a test user
        email = 'test@example.com'
        password = 'password123'
        user = User(email=email, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        # Simulate a login request with valid credentials
        response = self.client.post('/login', data={'email': email, 'password': password})
        self.assertEqual(response.status_code, 302)

        # Check the location header
        self.assertEqual(response.headers['Location'], '/')

        # Add more assertions as needed


    def test_login_incorrect_password(self):
        # Create a test user
        email = 'test@example.com'
        password = 'password123'
        user = User(email=email, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        # Simulate a login request with incorrect password
        response = self.client.post('/login', data={'email': email, 'password': 'wrongpassword'})
        self.assert200(response)
        # Add more assertions as needed

    def test_login_email_not_exist(self):
        # Simulate a login request with an email that does not exist
        response = self.client.post('/login', data={'email': 'nonexistent@example.com', 'password': 'password123'})
        self.assert200(response)

    def test_logout_route(self):
        with self.client:
            # Login the user
            response = self.client.post('/login', data=dict(email='test_user', password='test_password'))
            self.assertEqual(response.status_code, 302)

            # Check the location header
            self.assertEqual(response.headers['Location'], '/')  # Expecting redirect

            # Follow the redirect
            response = self.client.get('/', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            # Access the logout route
            response = self.client.get('/logout')
            self.assertEqual(response.status_code, 302)  # Expecting redirect

            self.assertFalse(current_user.is_authenticated)  # Ensure user is logged out




    def test_sign_up_route(self):
        with self.client:
            response = self.client.post('/sign-up', data=dict(
                email='new_user@example.com',
                firstName='New User',
                password1='test_password',
                password2='test_password'
            ))
            self.assertEqual(response.status_code, 302)  # Expecting redirect

            # Follow the redirect
            response = self.client.get(response.headers['Location'])
            self.assertEqual(response.status_code, 200)
            self.assertTrue(current_user.is_authenticated)  # Ensure user is logged in

            # Additional assertions to validate the created user in the database
            user = User.query.filter_by(email='new_user@example.com').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, 'new_user@example.com')
            self.assertEqual(user.first_name, 'New User')
            self.assertTrue(user.check_password('test_password'))  # Verify password

            # Clean up: delete the created user
            db.session.delete(user)
            db.session.commit()
