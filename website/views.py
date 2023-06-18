from flask import Blueprint, render_template #has a bunch of routes

views = Blueprint('views', __name__)

#name of the Blueprint
@views.route('/')
def home():
    return render_template("home.html")