from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favorites = db.relationship("Favorites", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize_user(self):
        return {
            "id": self.id,
            "email": self.email,
            "username":self.username,
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120))
    gender = db.Column(db.String(120))
    hair_color =  db.Column(db.String(70))
    eye_color =  db.Column(db.String(70))
    heigth =  db.Column(db.Integer)

    def __repr__(self):
        return '<Characters %r>' % self.id

    def serialize_characters(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender":self.gender,
            "hair_color":self.hair_color,
            "eye_color":self.eye_color,
            "heigth":self.heigth,
        }

class Planets(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120))
    terrain = db.Column(db.Integer)
    population = db.Column(db.Integer)
    gravity = db.Column(db.Integer)
    diameter = db.Column(db.Integer)

    def __repr__(self):
        return '<Planets %r>' % self.id

    def serialize_planets(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain":self.terrain,
            "population":self.population,
            "gravity":self.grativy,
            "diameter":self.diameter,
        }

class Favorites(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    fav_name =  db.Column(db.String(250),nullable = False)

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize_favorites(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "fav_name":self.fav_name,
        }
   
        

