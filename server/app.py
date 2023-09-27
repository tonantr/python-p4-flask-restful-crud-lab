#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

import pdb

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True

app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Home(Resource):

    def get(self):

        response_dict = {
            'message': 'Welcome !!!'
        }

        response = make_response(response_dict, 200)
        return response

api.add_resource(Home, '/')

class Plants(Resource):

    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)


api.add_resource(Plants, '/plants')


class PlantByID(Resource):

    def get(self, id):
        plant = Plant.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(plant), 200)
    
    def patch(sefl, id):
        
        record = Plant.query.filter_by(id=id).first()
        for attr, value in request.json.items():
            setattr(record, attr, value)
        
        db.session.commit()

        return make_response(record.to_dict(), 200)
    
    def delete(self, id):

        # pdb.set_trace()

        record = Plant.query.filter_by(id=id).first()

        if record:
            db.session.delete(record)
            db.session.commit()
            return '', 204
        else:
            return jsonify({'message': 'Record not found'}), 404


api.add_resource(PlantByID, '/plants/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
