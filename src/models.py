from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    username = db.Column(db.Boolean(120), unique=False, nullable=False)

class Characters(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120))
    gender = db.Column(db.String(120))
    hair_color =  db.Column(db.String(70))
    eye_color =  db.Column(db.String(70))
    heigth =  db.Column(db.Integer)

class Planets(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120))
    terrain = db.Column(db.Integer)
    population = db.Column(db.Integer)
    gravity = db.Column(db.Integer)
    diameter = db.Column(db.Integer)

# class Favorites(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     characters_id =Column(Integer,ForeignKey('characters.id'))
#     planets_id = Column(Integer,ForeignKey('planets.id'))
        

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

