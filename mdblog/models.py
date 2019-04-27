from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

# globalna premenna instancie
db = SQLAlchemy()

# trieda ktora bude dedit s db.model, takto vie sql alchemy ktore objekty budu mapovane do databazy
class Article(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String)
	content = db.Column(db.String)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, unique=True)
	password = db.Column(db.String)

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)