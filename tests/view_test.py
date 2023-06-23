import unittest
from flask import Flask
from flask_testing import TestCase
from website import views, db, models
from flask_login import LoginManager

class TestViews(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.register_blueprint(views.views)
        db.init_app(app)
        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(id):
            return models.User.query.get(int(id))
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_route(self):
        response = self.client.get('/')
        self.assert200(response)
        # Add more assertions to validate the response as needed

    def test_delete_note_route(self):
        response = self.client.post('/delete-note', json={'noteId': 1})
        self.assert200(response)
        # Add more assertions to validate the response as needed

if __name__ == '__main__':
    unittest.main()
