from. import mechanics_bp
from.schemas import Mechanic, mechanic_schema, mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import db
from sqlalchemy import select
from.schemas import login_schema
from app.extensions import cache, limiter
from app.utils.utils import encode_token, token_required


@mechanics_bp.route("/login", methods=['POST'])
def login():

    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Mechanic).where(Mechanic.email == email)
    mechanic = db.session.execute(query).scalars().first()

    if mechanic and mechanic.password == password:
        token = encode_token(mechanic.id, 'mechanic')

        response = {
            "status": "success",
            "message": "successfully logged in.",
            "token": token
        }

        print("Raw token:", token)
        return jsonify(response), 200
    else:
        return jsonify({"message": "Invalid email or password!"})

@mechanics_bp.route("/", methods=['POST'])
@limiter.limit('3 per hour')  #No more than 3 accounts should need to be made per hour
def create_mechanic():

    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_mechanic = Mechanic(name=mechanic_data['name'], email=mechanic_data['email'], password=mechanic_data['password'], phone=mechanic_data['phone'], salary=mechanic_data['salary'])

    db.session.add(new_mechanic)
    db.session.commit()

    return jsonify({"New mechanic has been created successfully": mechanic_schema.dump(new_mechanic)}),201

@mechanics_bp.route("/", methods=['GET'])
@cache.cached(timeout=180) #Caching the GET route because it would be utilized most frequently
def get_mechanics():

    query = select(Mechanic)
    result = db.session.execute(query).scalars().all()

    return jsonify({"Mechanics": mechanics_schema.dump(result)}), 200

@mechanics_bp.route("/", methods=['PUT'])
@token_required
def update_mechanic(user_id, role):

    query = select(Mechanic).where(Mechanic.id == user_id)
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

@mechanics_bp.route("/", methods=['DELETE'])
@token_required
def delete_mechanic(user_id, role):

    query = select(Mechanic).where(Mechanic.id == user_id)
    mechanic = db.session.execute(query).scalars().first()

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted mechanic with ID: {user_id}"}), 200

@mechanics_bp.route("/tickets-worked", methods=['GET'])
def service_tickets_worked():

    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    
    mechanics.sort(key=lambda mechanic:len(mechanic.service_tickets), reverse=True)

    return mechanics_schema.jsonify(mechanics), 200
