from flask_sqlalchemy import SQLAlchemy

# globalna premenna instancie
db = SQLAlchemy()

# trieda ktora bude dedit s db.model, takto vie sql alchemy ktore objekty budu mapovane do databazy
class Article(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String)
	content = db.Column(db.String)