from gis import db


# Defining classes for SQLAlchemy to be converted into SQL
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    affiliation = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, username, first_name, last_name, affiliation, password_hash, email):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.affiliation = affiliation
        self.password_hash = password_hash
        self.email = email

    # Function to output data as list of dictionaries, not as an object of a class
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Samples(db.Model):
    __tablename__ = 'samples'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    long = db.Column(db.Numeric(9, 6), nullable=False)
    lat = db.Column(db.Numeric(9, 6), nullable=False)
    sr = db.Column(db.Numeric(9, 6), nullable=False)
    sample_type = db.Column(db.String(40), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __init__(self, name, long, lat, sr, sample_type, number, user_id):
        self.name = name
        self.long = long
        self.lat = lat
        self.sr = sr
        self.sample_type = sample_type
        self.number = number
        self.user_id = user_id

    # Function to output data as list of dictionaries, not as an object of a class
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Settlements(db.Model):
    __tablename__ = 'settlements'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    long = db.Column(db.Numeric(9, 6), nullable=False)
    lat = db.Column(db.Numeric(9, 6), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __init__(self, name, location, long, lat, user_id):
        self.name = name
        self.location = location
        self.long = long
        self.lat = lat
        self.user_id = user_id

    # Function to output data as list of dictionaries, not as an object of a class
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
