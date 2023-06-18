from flask import Blueprint #has a bunch of routes

views = Blueprint('views', __name__)

#name of the Blueprint
@views.route('/')
def home():
    return "<h1>Test</h1>"