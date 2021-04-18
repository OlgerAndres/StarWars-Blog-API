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

# from flask_jwt_extended import create_access_token , get_jwt_identity , jwt_required , JWTManager


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


# app.config["JWT_SECRET_KEY"] = "JWT_SECRET_KEY"
# jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/test_user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/user', methods=['GET'])
def get_user():
     users = User.query.all()
     request = list(map(lambda user:user.serialize(),users))
     return jsonify(request),200  

@app.route('/register',methods=['POST'])
def create_register():
    username = request.json.get("username",None)
    email = request.json.get("email",None)
    password = request.json.get('password',None)
    if username is None:
        return jsonify({"msg": "No username was provided"}),400
    if email is None:
        return jsonify({"msg": "No email was provided"}),400
    if password is None:
        return jsonify({"msg" : "No email was provided"}),400
    user = User.query.filter_by(email=email,password=password).first()
    if user:
        return  jsonify({"msg" : "User already exists"}),401
    else:
        new_user = User()
        new_user.username = username
        new_user.email = email
        new_user.password = password

        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "User created succesfully"}),200   
    


@app.route('/characters/',methods=['GET'])
def get_characters():
    response_body = {
        "msg": "Hello, this is your GET /characters response "
    }
    return jsonify(response_body), 200

@app.route('/planets/',methods=['GET'])
def get_planets():
  response_body = {
        "msg": "Hello, this is your GET /planets response "
    }
  return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
