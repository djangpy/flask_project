from flask import Blueprint
from flask import render_template

main = Blueprint("main", __name__)

# CONTROLLERS
@main.route("/")  # Dekorator spoji funkciu index s adresou
def view_velcome_page():
	return render_template("mod_main/welcome_page.html", active='home')


@main.route("/about/")
def view_about_page():
	return render_template("mod_main/about.html")
