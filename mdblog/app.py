from flask import Flask
from flask import render_template

flask_app = Flask(__name__)


@flask_app.route("/")  # Dekorator spoji funkciu index s adresou
def index():
	return render_template("welcome_page.jinja")

@flask_app.route("/admin/")
def view_admin():
	return "Hello Administrator"