from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import g
from flask import flash
import sqlite3
import os

flask_app = Flask(__name__)

flask_app.config.from_pyfile("/vagrant/configs/default.py")

# ak sa nachadza env premenna mdblog_config v operac. syst environ 
# flask_app si pozrie automaticky configuracny subor MDBLOG_CONFIG kde je cesta k suboru a pouzije na dokonfigurovanie
if "MDBLOG_CONFIG" in os.environ:
	flask_app.config.from_envvar("MDBLOG_CONFIG")

@flask_app.route("/")  # Dekorator spoji funkciu index s adresou
def view_velcome_page():
	return render_template("welcome_page.jinja", active='home')

@flask_app.route("/about/")
def view_about_page():
	return render_template("about.jinja")

@flask_app.route("/articles/", methods=["GET"])
def view_articles_page():
	db = get_db()
	cur = db.execute("select * from articles order by id desc")
	articles = cur.fetchall()
	return render_template("articles.jinja", articles=articles)

@flask_app.route("/articles/", methods=["POST"])
def view_add_articles_page():
	db = get_db()
	cur = db.execute("insert into articles (title, content) values (?, ?)",
				[request.form.get("title"), request.form.get("content")])
	db.commit() #zapise do db
	flash("Article was saved", "alert-success")
	return redirect(url_for("view_articles_page"))

@flask_app.route("/admin/")
def view_admin_page():
	if "logged" not in session:
		flash("You must be logged in", "alert-danger")
		return redirect(url_for('view_login'))
	return render_template("admin.jinja")

@flask_app.route("/articles/<int:art_id>") #definujeme si premennu integer art_id
def view_article_page(art_id):
	db = get_db()
	cur = db.execute("select * from articles where id=(?)",[art_id])
	article = cur.fetchone() # dohladanie article v zozname articles podla id
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
		if username == flask_app.config["USERNAME"] and \
			 	password == flask_app.config["PASSWORD"]:
			session["logged"]=True
			flash("Login successful", "alert-success")
			return redirect(url_for('view_admin_page'))
		else:
			flash("Invalid credentials", "alert-danger")
			return redirect(url_for('view_login'))

@flask_app.route("/logout/", methods=["POST"])
def logout_user():
	session.pop("logged")
	flash("Logout successful", "alert-success")
	return redirect(url_for("view_velcome_page"))

## UTILS
def connect_db():
    rv = sqlite3.connect(flask_app.config["DATABASE"])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@flask_app.teardown_appcontext
def close_db(error):
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()

def init_db(app):
    with app.app_context():
        db = get_db()
        with open("mdblog/schema.sql", "r") as fp:
            db.cursor().executescript(fp.read())
        db.commit()

