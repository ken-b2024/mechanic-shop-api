from.import customers_bp
from.schemas import Customer, customer_schema, customers_schema, login_schema
from app.blueprints.service_tickets.schemas import ServiceTicket, return_service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import db
from sqlalchemy import select
from app.extensions import limiter, cache
from app.utils.utils import encode_token, token_required
from app.extensions import bcrypt


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

    if customer and bcrypt.check_password_hash(customer.password, password):
        token = encode_token(customer.id, 'customer')

        response = {
            "status": "success",
            "message": "successfully logged in.",
            "token": token
        }

        return jsonify(response), 200
    else:
        return jsonify({"message": "Invalid email or password!"}), 400

@customers_bp.route("/", methods=['POST'])
def create_customer():

    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    hashed_pw = bcrypt.generate_password_hash(customer_data['password']).decode('utf-8')
    new_customer = Customer(name=customer_data['name'], email=customer_data['email'], password=hashed_pw, phone=customer_data['phone'], make_model=customer_data['make_model'], VIN=customer_data['VIN'])

    db.session.add(new_customer)
    db.session.commit()

    return jsonify({"New customer has been created successfully": customer_schema.dump(new_customer)}),201

@customers_bp.route("/", methods=['GET'])
@limiter.limit('5 per hour')
@cache.cached(timeout=180)
def get_customers():

    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Customer)
        customers = db.paginate(query, page=page, per_page=per_page)
        return customers_schema.jsonify(customers), 200
    except:
        query = select(Customer)
        result = db.session.execute(query).scalars().all()
        return jsonify({"Customers": customers_schema.dump(result)}), 200

@customers_bp.route("/my-tickets", methods=['GET'])
def get_customer_tickets(*args, **kwargs):
    user_id = kwargs.get('user_id')
    role = kwargs.get('role')

    query = select(ServiceTicket).where(ServiceTicket.customer_id == user_id)
    tickets = db.session.execute(query).scalars().all()

    return jsonify({"Tickets": return_service_tickets_schema.dump(tickets)}), 200

@customers_bp.route("/", methods=['PUT'])
@token_required
@limiter.limit('3 per hour')
def update_customer(user_id, role):

    query = select(Customer).where(Customer.id == user_id)
    customer = db.session.execute(query).scalars().first()

    if customer == None:
        return jsonify({"message": "Invalid customer ID"})
    
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in customer_data.items():
        if value in [None, ""]:
            continue
        if field == 'password':
            value = bcrypt.generate_password_hash(value).decode("utf-8")
        setattr(customer, field, value)

    db.session.commit()
    return jsonify({"Customer has been successfully updated": customer_schema.dump(customer)}), 200

@customers_bp.route("/", methods=['DELETE'])
@token_required
def delete_customer(user_id, role):

    query = select(Customer).where(Customer.id == user_id)
    customer = db.session.execute(query).scalars().first()

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted customer with ID: {user_id}"})