from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from flask import Flask, jsonify, make_response

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)
app = Flask(__name__)

# Add models here
class Earthquake(db.Model, SerializerMixin):
  __tablename__ = 'earthquakes'

  id = db.Column(db.Integer, primary_key=True)
  magnitude = db.Column(db.Float)
  location = db.Column(db.String)
  year = db.Column(db.Integer)

  def __repr__(self):
    return f"<Earthquake {self.id}, {self.magnitude}, {self.location}, {self.year}>"

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    with db.session() as session:
        earthquakes = session.query(Earthquake).filter_by(magnitude=magnitude).all()
    if earthquakes:
        return jsonify({
            'count': len(earthquakes),
            'quakes': [{'id': quake.id, 'magnitude': quake.magnitude, 'location': quake.location, 'year': quake.year} for quake in earthquakes]
        })
    else:
        return make_response(jsonify({'count': 0, 'quakes': [], 'message': f'No earthquakes found with magnitude {magnitude}.'}), 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)