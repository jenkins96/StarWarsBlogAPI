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
from models import db, User, Characters, Planets, PlanetsFavorites, CharactersFavorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_users():

    result = User.query.all()
    # map the results and your list of users  inside of the all_users variable
    all_users = list(map(lambda x: x.serialize(), result))


    return jsonify(all_users), 200

@app.route('/characters', methods=['GET'])
def get_characters():

    result = Characters.query.all()
    # map the results and your list of users  inside of the all_users variable
    all_characters = list(map(lambda x: x.serialize(), result))


    return jsonify(all_characters), 200

@app.route('/planets', methods=['GET'])
def get_planets():

    result = Planets.query.all()
    # map the results and your list of users  inside of the all_users variable
    all_planets = list(map(lambda x: x.serialize(), result))


    return jsonify(all_planets), 200

"""------------------------------------------------------- 
                    FAVORITES SECTION
-------------------------------------------------------"""

@app.route('/user/<int:id>/favorites', methods=['GET'])
def get_user_favorites(id):
    
    item = User.query.get(id)

    if item is None:
        raise APIException('User not found', status_code=404)

    return jsonify(item.serializeFavorites()), 200

@app.route('/user/<int:id>/favorites', methods=['POST'])
def add_favorites(id):
    # get all the people
    item = User.query.get(id)
    body = request.get_json()

    if item is None:
        raise APIException('User not found', status_code=404)
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'id' not in body:
        raise APIException("ID is not defined", status_code=400)

    if(body['Type'] == "Planet"):
        planet_id = Planet.query.get(body["id"])
        if planet_id is None:
            raise APIException('Planet does not exists', status_code=404)
        else:
            favPlanet = like_planet(userid = id, planetid = body["id"])
            db.session.add(favPlanet)
            db.session.commit()
    else:
        character_id = Characters.query.get(body["id"])
        if character_id is None:
            raise APIException('Character does not exists', status_code=404)
        else:
            favCharacter = like_character(userid = id, characterid = body["id"])
            db.session.add(favCharacter)
            db.session.commit()
            
    return "OK", 200



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
