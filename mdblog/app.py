from flask import Flask
from flask import render_template

flask_app = Flask(__name__)


@flask_app.route("/")  # Dekorator spoji funkciu index s adresou
def view_velcome_page():
	return render_template("welcome_page.jinja", active='home')

@flask_app.route("/about/")
def view_about_page():
	return render_template("about.jinja")

@flask_app.route("/articles/")
def view_articles_page():
	return render_template("articles.jinja")

@flask_app.route("/admin/")
def view_admin_page():
	return render_template("admin.jinja")

