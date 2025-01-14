#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# Add models here
class Earthquake(db.Model, SerializerMixin):
    __tablename__ = 'earthquakes'

    id = db.Column(db.Integer, primary_key=True)
    magnitude = db.Column(db.Float)
    location = db.Column(db.String)
    year = db.Column(db.Integer)

    def __repr__(self):
        return f"<Earthquake {self.id}, {self.magnitude}, {self.location}, {self.year}>"

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Get earthquake by ID
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    earthquake = db.session.get(Earthquake, id)
    if earthquake:
        return jsonify(earthquake.to_dict())
    else:
        return make_response(jsonify({'message': f'Earthquake {id} not found.'}), 404)

# Get earthquakes by magnitude (>= specified magnitude)
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    with db.session() as session:
        earthquakes = session.query(Earthquake).filter(Earthquake.magnitude >= magnitude).all()
    if earthquakes:
        return jsonify({
            'count': len(earthquakes),
            'quakes': [quake.to_dict() for quake in earthquakes]
        }), 200
    else:
        return jsonify({'count': 0, 'quakes': []}), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)