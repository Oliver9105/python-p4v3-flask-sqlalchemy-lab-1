#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Get earthquake by ID
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    earthquake = db.session.get(Earthquake, id)
    if earthquake:
        return jsonify({
            'id': earthquake.id,
            'magnitude': earthquake.magnitude,
            'location': earthquake.location,
            'year': earthquake.year
        })
    else:
        return make_response(jsonify({'message': f'Earthquake {id} not found.'}), 404)

# Get earthquakes by magnitude (>= specified magnitude)
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    with db.session() as session:
       earthquakes = db.session.query(Earthquake).filter(Earthquake.magnitude >= magnitude).all()
    if earthquakes:
        return jsonify({
            'count': len(earthquakes),
            'quakes': [{'id': quake.id, 'magnitude': quake.magnitude, 'location': quake.location, 'year': quake.year} for quake in earthquakes]
        }), 200
    else:
        return jsonify({'count': 0, 'quakes': []}), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
