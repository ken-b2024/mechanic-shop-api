from app.models import ServiceTicket
from app.blueprints.mechanics.schemas import MechanicSchema
from app.extensions import ma
from marshmallow import fields, post_dump


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested(MechanicSchema, many=True)
    mechanic_ids = fields.List(fields.Int(), required=False)
    customer_id = fields.Int(required=True)

    class Meta:
        model = ServiceTicket
        fields= ("service_desc", "customer_id", "mechanic_ids", "mechanics")

    @post_dump
    def add_mechanic_ids(self, data, **kwargs):
        if 'mechanics' in data:
            data['mechanic_ids'] = [mech['id'] for mech in data['mechanics']]
        return data

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)