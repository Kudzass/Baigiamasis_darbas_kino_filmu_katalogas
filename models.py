from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Zanras(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pavadinimas = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return self.pavadinimas

class Filmas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pavadinimas = db.Column(db.String(200), nullable=False)
    isleidimo_data = db.Column(db.Date, nullable=False)
    rezisierius = db.Column(db.String(100), nullable=False)
    imdb = db.Column(db.Float)
    zanras_id = db.Column(db.Integer, db.ForeignKey('zanras.id'))
    zanras = db.relationship('Zanras', backref='filmai')
