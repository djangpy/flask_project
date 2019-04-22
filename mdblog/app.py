from flask import Flask
from flask import render_template

from .database import articles

flask_app = Flask(__name__)


@flask_app.route("/")  # Dekorator spoji funkciu index s adresou
def view_velcome_page():
	return render_template("welcome_page.jinja", active='home')

@flask_app.route("/about/")
def view_about_page():
	return render_template("about.jinja")

@flask_app.route("/articles/")
def view_articles_page():
	return render_template("articles.jinja", articles=articles.items())

@flask_app.route("/admin/")
def view_admin_page():
	return render_template("admin.jinja")

@flask_app.route("/articles/<int:art_id>") #definujeme si premennu integer art_id
def view_article_page(art_id):
	article = articles.get(art_id) # dohladanie article v zozname articles podla id
	if article:
		return render_template("article.jinja", article=article)
	return render_template("article_not_found.jinja", art_id=art_id)