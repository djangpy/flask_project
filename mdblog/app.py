from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import g
from flask import flash

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import TextAreaField
from wtforms.validators import InputRequired

import sqlite3
import os

flask_app = Flask(__name__)

flask_app.config.from_pyfile("/vagrant/configs/default.py")

# ak sa nachadza env premenna mdblog_config v operac. syst environ 
# flask_app si pozrie automaticky configuracny subor MDBLOG_CONFIG kde je cesta k suboru a pouzije na dokonfigurovanie
if "MDBLOG_CONFIG" in os.environ:
    flask_app.config.from_envvar("MDBLOG_CONFIG")


# FORMS
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class ArticleForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Content")


# CONTROLLERS
@flask_app.route("/")  # Dekorator spoji funkciu index s adresou
def view_velcome_page():
    return render_template("welcome_page.html", active='home')


@flask_app.route("/about/")
def view_about_page():
    return render_template("about.html")


# ARTICLES
@flask_app.route("/articles/", methods=["GET"])
def view_articles_page():
    db = get_db()
    cur = db.execute("select * from articles order by id desc")
    articles = cur.fetchall()
    return render_template("articles.html", articles=articles)


@flask_app.route("/articles/new/", methods=["GET"])
def view_add_article():
    if "logged" not in session:
        return redirect(url_for("view_login"))
    form = ArticleForm()
    return render_template("article_editor.html", form=form)


@flask_app.route("/articles/", methods=["POST"])
def add_article():
    if "logged" not in session:
        return redirect(url_for("view_login"))

    db = get_db()
    db.execute("insert into articles (title, content) values (?, ?)",
               [request.form.get("title"), request.form.get("content")])
    db.commit()
    flash("Article was saved", "alert-success")
    return redirect(url_for("view_articles_page"))


@flask_app.route("/admin/")
def view_admin_page():
    if "logged" not in session:
        flash("You must be logged in", "alert-danger")
        return redirect(url_for('view_login'))
    return render_template("admin.html")


@flask_app.route("/articles/<int:art_id>")  # definujeme si premennu integer art_id
def view_article_page(art_id):
    db = get_db()
    cur = db.execute("select * from articles where id=(?)", [art_id])
    article = cur.fetchone()  # dohladanie article v zozname articles podla id
    if article:
        return render_template("article.html", article=article)
    return render_template("article_not_found.html", art_id=art_id)


@flask_app.route("/articles/<int:art_id>/edit/", methods=["GET"])
def view_article_editor(art_id):
    if "logged" not in session:
        return redirect(url_for("view_login"))
    db = get_db()
    cur = db.execute("select * from articles where id=(?)", [art_id])
    article = cur.fetchone()
    if article:
        form = ArticleForm()
        form.title.data = article["title"]
        form.content.data = article["content"]
        return render_template("article_editor.html", form=form, article=article)
    return render_template("article_not_found.html", art_id=art_id)


@flask_app.route("/articles/<int:art_id>/", methods=["POST"])
def edit_article(art_id):
    if "logged" not in session:
        return redirect(url_for("view_login"))
    db = get_db()
    cur = db.execute("select * from articles where id=(?)", [art_id])
    article = cur.fetchone()
    if article:
        edit_form = ArticleForm(request.form)
        if edit_form.validate():
            db.execute("update articles set title=?, content=? where id=?",
                       [edit_form.title.data, edit_form.content.data, art_id])
            db.commit()
            flash("Edit saved", "alert-success")
            return redirect(url_for("view_article_page", art_id=art_id))
        else:
            for error in login_form.errors:
                flash("{} is missing".format(error), "alert-danger")
            return redirect(url_for("view_login"))


@flask_app.route("/login/", methods=['GET'])
def view_login():
    login_form = LoginForm()
    return render_template("login.html", form=login_form)


@flask_app.route("/login/", methods=["POST"])
def login_user():
    login_form = LoginForm(request.form)
    if login_form.validate():
        if login_form.username.data == flask_app.config["USERNAME"] and \
                login_form.password.data == flask_app.config["PASSWORD"]:
            session["logged"] = True
            flash("Login successful", "alert-success")
            return redirect(url_for("view_admin_page"))
        else:
            flash("Invalid credentials", "alert-danger")
            return render_template("login.html", form=login_form)
    else:
        for error in login_form.errors:
            flash("{} is missing".format(error), "alert-danger")
        return redirect(url_for("view_login"))


@flask_app.route("/logout/", methods=["POST"])
def logout_user():
    session.pop("logged")
    flash("Logout successful", "alert-success")
    return redirect(url_for("view_velcome_page"))


# UTILS
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
