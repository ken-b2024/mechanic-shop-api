from app.models import ServiceTicket
from app.extensions import ma
from marshmallow import fields


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanic_ids = fields.List(fields.Int(), required=False)
    customer_id = fields.Int(required=True)

    class Meta:
        model = ServiceTicket
        fields= ("mechanic_ids", "service_desc", "customer_id")

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)