from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

    


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), unique=False, nullable=False)
    last_name = db.Column(db.String(250), unique=False, nullable=False)
    username = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    #RELATIONSHIPS
    like_character = db.relationship("CharactersFavorites", backref='user', lazy=True)
    like_planet = db.relationship("PlanetsFavorites", backref='user', lazy=True)


    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "like_character": list(map(lambda y: y.serializeForUser(), self.like_character)),
            "like_planet": list(map(lambda y: y.serializeForUser(), self.like_planet)),
            # do not serialize the password, its a security breach
        }
    def serializeFavorites(self):
        return {
            "id": self.id,
            "like_character": list(map(lambda y: y.serializeForUser(), self.charactersFavorites)),
            "like_planet": list(map(lambda y: y.serializeForUser(), self.planetsfavorites)),
            # do not serialize the password, its a security breach
        }

# PLANETS TABLE
 
class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    rotation_period = db.Column(db.Integer, unique=False,nullable=False)
    orbital_period = db.Column(db.Integer, unique=False,nullable=False)
    diameter = db.Column(db.Integer, unique=False,nullable=False)
    gravity = db.Column(db.String(250), unique=False, nullable=False)
    population = db.Column(db.Integer, unique=False,nullable=False)
    #RELATIONSHIP
    like_planet = db.relationship("PlanetsFavorites", backref='Planets', lazy=True) 

    def __repr__(self):
        return '<Planets %r>' % self.name 

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "population": self.population,
            "like_planet": list(map(lambda y: y.serializeForPlanet(), self.like_planet)),
            # do not serialize the password, its a security breach
        }

# CHARACTERS TABLE
  
class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    height = db.Column(db.Integer, unique=False,nullable=False)
    mass = db.Column(db.Integer, unique=False,nullable=False)
    hair_color = db.Column(db.String(250), unique=False, nullable=False)
    skin_color = db.Column(db.String(250), unique=False, nullable=False)
    birth_year = db.Column(db.String(250), unique=False, nullable=False)
   # RELATIONSHIP
    like_character = db.relationship("CharactersFavorites", backref='characters', lazy=True)

    def __repr__(self):
        return '<Characters %r>' % self.name 

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "birth_year": self.birth_year,
            "like_character": list(map(lambda y: y.serializeForCharacter(), self.like_character)),
            # do not serialize the password, its a security breach
        }


# PLANETS FAVORITES TABLE 
class PlanetsFavorites(db.Model):
    __tablename__ = 'planetsfavorites'
    id = db.Column(db.Integer, primary_key=True)
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"))

    def __repr__(self):
        return '<PlanetsFavorites %r>' % self.user_id
    # Revisar esto...
    def serializeForUser(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id,
        }
    def serializeForPlanet(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }


# CHARACTERS FAVORITES TABLE
class CharactersFavorites(db.Model):
    __tablename__ = 'charactersFavorites'
    id = db.Column(db.Integer, primary_key=True)
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("characters.id"))

    def __repr__(self):
        return '<CharactersFavorites %r>' % self.user_id 

    def serializeForUser(self):
        return {
            "id": self.id,
            #"user_id": self.user_id,
            "character_id": self.character_id,
            # do not serialize the password, its a security breach
        }
    def serializeForCharacter(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            #"character_id": self.character_id,
        }
        