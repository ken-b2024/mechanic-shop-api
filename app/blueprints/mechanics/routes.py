from. import mechanics_bp
from.schemas import Mechanic, mechanic_schema, mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import db
from sqlalchemy import select, delete


@mechanics_bp.route("/", methods=['POST'])
def create_mechanic():

    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_mechanic = Mechanic(name=mechanic_data['name'], email=mechanic_data['email'], phone=mechanic_data['phone'], salary=mechanic_data['salary'])

    db.session.add(new_mechanic)
    db.session.commit()

    return jsonify({"New mechanic has been created successfully": mechanic_schema.dump(new_mechanic)}),201

@mechanics_bp.route("/", methods=['GET'])
def get_mechanics():

    query = select(Mechanic)
    result = db.session.execute(query).scalars().all()

    return jsonify({"Mechanics": mechanics_schema.dump(result)}), 200

@mechanics_bp.route("/<int:mechanic_id>", methods=['PUT'])
def update_mechanic(mechanic_id):

    query = select(Mechanic).where(Mechanic.id == mechanic_id)
    mechanic = db.session.execute(query).scalars().first()

    if mechanic == None:
        return jsonify({"message": "Invalid mechanic ID"})
    
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in mechanic_data.items():
        setattr(mechanic,field, value)

    db.session.commit()
    return jsonify({"Mechanic has been successfully updated": mechanic_schema.dump(mechanic)}), 200

@mechanics_bp.route("/<int:mechanic_id>", methods=['DELETE'])
def delete_mechanic(mechanic_id):

    query = select(Mechanic).where(Mechanic.id == mechanic_id)
    mechanic = db.session.execute(query).scalars().first()

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted mechanic with ID: {mechanic_id}"})