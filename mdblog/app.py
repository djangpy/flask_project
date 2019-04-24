from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from .database import articles

flask_app = Flask(__name__)
flask_app.secret_key  = '(\xe2\x10.\xb3\xdfL[d\x1f\x93\x90\xc2,\xffL\x03N\xc7[G\xa0\xd6\x83'


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
	if "logged" not in session:
		return redirect(url_for('view_login'))
	return render_template("admin.jinja")

@flask_app.route("/articles/<int:art_id>") #definujeme si premennu integer art_id
def view_article_page(art_id):
	article = articles.get(art_id) # dohladanie article v zozname articles podla id
	if article:
		return render_template("article.jinja", article=article)
	return render_template("article_not_found.jinja", art_id=art_id)

@flask_app.route("/login/", methods=['GET'])
def view_login():
		return render_template("login.jinja")

@flask_app.route("/login/", methods=['POST'])
def login_user():
	if request.method == "POST":
		username=request.form["username"]
		password=request.form["password"]
		if username == "admin" and password == "admin":
			session["logged"]=True
			return redirect(url_for('view_admin_page'))
		else:
			return redirect(url_for('view_login'))

@flask_app.route("/logout/", methods=["POST"])
def logout_user():
	session.pop("logged")
	return redirect(url_for("view_velcome_page"))