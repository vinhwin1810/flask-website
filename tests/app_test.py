import unittest
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from website import create_app, db, models
from os import path

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Database test riêng biệt
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_create_database(self):
        DB_NAME = "database.db"
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            self.assertTrue(path.exists('instance/' + DB_NAME))

    def test_example(self):
        with self.app.app_context():
            # Thực hiện test case trong một transaction
            with db.session.begin_nested():
                # Thực hiện các thay đổi dữ liệu trong transaction
                # Không ghi hoặc thay đổi dữ liệu trong database chính
                # Ví dụ:
                # Tạo đối tượng và lưu vào database test
                user = models.User(email="test_user", password="test_password")
                db.session.add(user)

                # Kiểm tra dữ liệu trước khi commit
                result = models.User.query.filter_by(email="test_user").first()
                self.assertIsNotNone(result)
                self.assertEqual(result.email, "test_user")
                self.assertEqual(result.password, "test_password")

            # Kiểm tra dữ liệu trong nested transaction trước khi commit
            result_nested = models.User.query.filter_by(email="test_user").first()
            self.assertIsNotNone(result_nested)

            # Thực hiện kiểm tra trong một nested transaction khác để kiểm tra dữ liệu trong database chính
            with db.session.begin_nested():
                # Kiểm tra dữ liệu trong database chính (không thay đổi)
                result_main_db = models.User.query.filter_by(email="test_user").first()
                self.assertIsNone(result_main_db)
