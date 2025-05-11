from.import customers_bp
from.schemas import Customer, customer_schema, customers_schema, login_schema
from app.blueprints.service_tickets.schemas import ServiceTicket, return_service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import db
from sqlalchemy import select
from app.extensions import limiter, cache
from app.utils.utils import encode_token, token_required


@customers_bp.route("/login", methods=['POST'])
def login():

    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.email == email)
    customer = db.session.execute(query).scalars().first()

    if customer and customer.password == password:
        token = encode_token(customer.id, 'customer')

        response = {
            "status": "success",
            "message": "successfully logged in.",
            "token": token
        }

        return jsonify(response), 200
    else:
        return jsonify({"message": "Invalid email or password!"})

@customers_bp.route("/", methods=['POST'])
@limiter.limit('3 per hour')
def create_customer():

    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_customer = Customer(name=customer_data['name'], email=customer_data['email'], password=customer_data['password'], phone=customer_data['phone'], make_model=customer_data['make_model'], VIN=customer_data['VIN'])

    db.session.add(new_customer)
    db.session.commit()

    return jsonify({"New customer has been created successfully": customer_schema.dump(new_customer)}),201

@customers_bp.route("/", methods=['GET'])
@limiter.limit('5 per hour')
@cache.cached(timeout=180)
def get_customers():

    query = select(Customer)
    result = db.session.execute(query).scalars().all()
    return jsonify({"Customers": customers_schema.dump(result)}), 200

@customers_bp.route("/my-tickets", methods=['GET'])
@token_required
def get_customer_tickets(customer_id):

    query = select(ServiceTicket).where(ServiceTicket.customer_id == customer_id)
    tickets = db.session.execute(query).scalars().all()

    return jsonify({"Tickets": return_service_tickets_schema.dump(tickets)}), 200

@customers_bp.route("/<int:customer_id>", methods=['PUT'])
@limiter.limit('3 per hour')
def update_customer(customer_id):

    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()

    if customer == None:
        return jsonify({"message": "Invalid customer ID"})
    
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in customer_data.items():
        setattr(customer, field, value)

    db.session.commit()
    return jsonify({"Customer has been successfully updated": customer_schema.dump(customer)}), 200

@customers_bp.route("/", methods=['DELETE'])
@token_required
def delete_customer(customer_id):

    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted customer with ID: {customer_id}"})