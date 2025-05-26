from.import inventory_items_bp
from.schemas import Inventory, inventory_item_schema, inventory_items_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import db, Inventory
from sqlalchemy import select



@inventory_items_bp.route("/", methods=['POST'])
def create_inventory_item():

    try:
        inventory_data = inventory_item_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_inventory_item = Inventory(name=inventory_data['name'], price=inventory_data['price'])

    db.session.add(new_inventory_item)
    db.session.commit()

    return jsonify({"New inventory item has been created successfully": inventory_item_schema.dump(new_inventory_item)}),201

@inventory_items_bp.route("/", methods=['GET'])
def get_inventory_items():

    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Inventory)
        inventory = db.paginate(query, page=page, per_page=per_page)
        return inventory_items_schema.jsonify(inventory), 200
    except:
        query = select(Inventory)
        result = db.session.execute(query).scalars().all()
        return jsonify({"Inventory Items": inventory_items_schema.dump(result)}), 200

@inventory_items_bp.route("/<int:inventory_item_id>", methods=['PUT'])
def update_inventory(inventory_item_id):

    query = select(Inventory).where(Inventory.id == inventory_item_id)
    inventory_item = db.session.execute(query).scalars().first()

    if inventory_item == None:
        return jsonify({"message": "Invalid inventory item ID"})
    
    try:
        inventory_data = inventory_item_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in inventory_data.items():
        setattr(inventory_item, field, value)

    db.session.commit()
    return jsonify({"inventory item has been successfully updated": inventory_item_schema.dump(inventory_item)}), 200

@inventory_items_bp.route("/<int:inventory_item_id>", methods=['DELETE'])
def delete_inventory(inventory_item_id):

    query = select(Inventory).where(Inventory.id == inventory_item_id)
    inventory_item = db.session.execute(query).scalars().first()

    db.session.delete(inventory_item)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted inventory item with ID: {inventory_item_id}"}),200