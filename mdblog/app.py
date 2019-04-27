from flask import Flask
from flask import render_template
from .models import db
from .models import User
from .mod_main import main
from .mod_blog import blog
from .mod_admin import admin

import os

flask_app = Flask(__name__)

flask_app.config.from_pyfile("/vagrant/configs/default.py")

# ak sa nachadza env premenna mdblog_config v operac. syst environ 
# flask_app si pozrie automaticky configuracny subor MDBLOG_CONFIG kde je cesta k suboru a pouzije na dokonfigurovanie
if "MDBLOG_CONFIG" in os.environ:
	flask_app.config.from_envvar("MDBLOG_CONFIG")

db.init_app(flask_app)

flask_app.register_blueprint(main)
flask_app.register_blueprint(blog)
flask_app.register_blueprint(admin)

@flask_app.errorhandler(500)
def internal_server_error(error):
	return render_template("errors/500.html"), 500

@flask_app.errorhandler(404)
def internal_server_error(error):
	return render_template("errors/404.html"), 404


# CLII COMMAND
def init_db(app):
	with app.app_context():
		db.create_all()
		print("database inicialized")

		default_user = User(username="admin")
		default_user.set_passwrod("admin")

		db.session.add(default_user)
		db.session.commit()
		print("default user was created")
