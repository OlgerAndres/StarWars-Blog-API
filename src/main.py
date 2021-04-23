"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Characters,Planets,Favorites

from flask_jwt_extended import create_access_token , get_jwt_identity , jwt_required , JWTManager
#Debo escribir en consola el comando  pipenv install flask-jwt-extended
import  datetime


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


app.config["JWT_SECRET_KEY"] = "JWT_SECRET_KEY"
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#Endpoints de users------------------------------------------------------------Endpoints of users
@app.route('/test_user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/user', methods=['GET'])
def get_users():
    data = jsonify(User.get_users())
    return data

@app.route('/login',methods=['POST'])
def login():
    if request.method == "POST":
        username =  request.json["username"]
        password = request.json["password"]

        if not username:
            return jsonify({"Error":"usarname Invalid"}), 400
        if not password:
            return jsonify({"Error":"Password Invalid"}),400
        
        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({"Error":"User not found"}),400
        #Create Tokken
        expiration_date = datetime.timedelta(days=1)
        access_token = create_access_token(identity=username,expires_delta=expiration_date)

        request_body = {
            "user":user.serialize(),
            "token":access_token
        }

        return jsonify(request_body),200
        
@app.route('/register', methods=['POST'])
def register_user():
    username = request.json.get("username",None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if username is None:
        return jsonify({"msg":"No username was provided"}),400
    if email is None:
        return jsonify({"msg": "No email was provided"}), 400
    if password is None:
        return jsonify({"msg": "No password was provided"}), 400
    
    user = User.query.filter_by(username=username,email=email, password=password).first()
    if user:
        # the user was not found on the database
        return jsonify({"msg": "User already exists"}), 401
    else:
        new_user = User()
        new_user.username = username
        new_user.email = email
        new_user.password = password

        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "User created successfully"}), 200


@app.route('/users/<int:id>', methods=['GET'])
def  user_id(id):
     user = User.query.filter_by(id=id).first()
     if user is None:
        raise APIException("msg: User not found",status_code=404)
     request = user.serialize()
     return jsonify(request),200

@app.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def  delete_user(id):
    current_user = get_jwt_identity()
    user1 = User.query.get(id)
    if user1 is None:
        raise APIException("User is not found",status_code=404)
    db.session.delete(user1)
    db.session.commit()
    return jsonify({"Succesfully":current_user}),200

@app.route('/users/<int:id>', methods = ['PUT'])
def update_user(id):
    user1 = User.query.get(id)
    username = request.json['username']
    email = request.json['email']

    user1.username = username
    user1.email = email
    db.session.commit()
   
    return jsonify(user1.serialize()), 200
   

#Endpoints of users---------------------------------------------------------------Endpoints of users


#Endpoints of characters----------------------------------------------------------Endpoints of characters

@app.route('/characters', methods=['GET'])
def get_characters():
    data = jsonify(Characters.get_characters())
    return data


@app.route('/character/<int:id>', methods=['GET'])
def  characters_id(id):
     character = Characters.query.filter_by(id=id).first()
     if character is None:
        raise APIException("msg: character not found",status_code=404)
     request = character.serialize()
     return jsonify(request),200

#Endpoints of characters----------------------------------------------------------Endpoints of characters

#Endpoints of planets----------------------------------------------------------Endpoints of planets
@app.route('/planets', methods=['GET'])
def get_planets():
    data = jsonify(Planets.get_planets())
    return data

@app.route('/planet/<int:id>', methods=['GET'])
def planets_id(id):
     planet = Planets.query.filter_by(id=id).first()
     if planet is None:
        raise APIException("msg: planet not found",status_code=404)
     request = planet.serialize()
     return jsonify(request),200
#Endpoints of planets----------------------------------------------------------Endpoints of planets

@app.route('/favorites', methods=['GET'])
@jwt_required()
def get_favorites():   
     current_user_id = get_jwt_identity()
     all_favorites = Favorites.query.filter_by(user_id = current_user_id)
     all_favorites = list(map(lambda x: x.serialize(),all_favorites))
     return jsonify(all_favorites),200
#Endpoints of favorites--------------------------------------------------------Endpoints of favorites
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
