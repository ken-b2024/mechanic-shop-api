from.import service_tickets_bp
from.schemas import service_ticket_schema, return_service_ticket_schema, return_service_tickets_schema, edit_service_ticket_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import db, Mechanic, ServiceTicket
from sqlalchemy import select
from app.extensions import cache, limiter


@service_tickets_bp.route("/", methods=['POST'])
@limiter.limit('10 per hour')  #The mechanic shop is only able to handle a maximum of 10 new tickets per hour
def create_service_ticket():

    try:
        ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_service_ticket = ServiceTicket(customer_id=ticket_data['customer_id'], service_desc=ticket_data['service_desc'])

    mechanic_ids = ticket_data.get('mechanic_ids', [])
    for mechanic_id in mechanic_ids:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalar()
        if mechanic:
            new_service_ticket.mechanics.append(mechanic)
        else:
            return jsonify({"message": "Invalid mechanic ID"})

    db.session.add(new_service_ticket)
    db.session.commit()

    return jsonify({"New service ticket has been created successfully": return_service_ticket_schema.dump(new_service_ticket)}), 201

@service_tickets_bp.route("/", methods=['GET'])
@cache.cached(timeout=180) #Caching the GET route because it would be utilized most frequently
def get_service_tickets():

    query = select(ServiceTicket)
    result = db.session.execute(query).scalars().all()

    return jsonify({"Service Tickets": return_service_tickets_schema.dump(result)}), 200

@service_tickets_bp.route("/<int:service_ticket_id>", methods=['PUT'])
def edit_service_ticket(service_ticket_id):

    try:
        ticket_edits = edit_service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(ServiceTicket).where(ServiceTicket.id == service_ticket_id)
    service_ticket = db.session.execute(query).scalars().first()

    if not service_ticket:
        return jsonify({"error": f"ServiceTicket with id {service_ticket_id} not found"}), 404
    
    for field, value in ticket_edits.items():
        setattr(service_ticket,field, value)

    for mechanic_id in ticket_edits['add_mechanic_ids']:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if mechanic and mechanic not in service_ticket.mechanics:
            service_ticket.mechanics.append(mechanic)
    
    for mechanic_id in ticket_edits['remove_mechanic_ids']:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if mechanic and mechanic in service_ticket.mechanics:
            service_ticket.mechanics.remove(mechanic)

    db.session.commit()
    return return_service_ticket_schema.jsonify(service_ticket)
