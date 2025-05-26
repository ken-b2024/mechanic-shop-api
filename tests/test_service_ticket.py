from app import create_app
from app.models import db, ServiceTicket, Inventory
from app.utils.utils import encode_token
import unittest


class TestServiceTicket(unittest.TestCase):


    def setUp(self):
        self.app = create_app("TestingConfig")
        self.ticket = ServiceTicket(
            customer_id = 1,
            service_desc = 'Oil change. Tire rotation'
        )
        self.inventory = Inventory(
            id=5,
            name="Brake Pad", 
            price=29.99
        )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.ticket)
            db.session.add(self.inventory)
            db.session.commit()
        self.client = self.app.test_client()


    def test_create_ticket(self):

        ticket_payload = {
            'customer_id': 1,
            'service_desc': 'Oil change. Tire rotation'
        }

        response = self.client.post('/servicetickets/', json=ticket_payload)

        self.assertEqual(response.status_code, 201)


    def test_invalid_retrieval(self):

        response = self.client.get('/service-tickets/')

        self.assertEqual(response.status_code, 404)


    def test_invalid_update(self):
        update_payload = {
            "remove_mechanic_ids": [1],
            "service_desc": "Oil change, Tire rotation, air filter replcement"
        }

        response = self.client.put('/servicetickets/1', json=update_payload)

        self.assertEqual(response.status_code, 400)


    def test_add_part(self):
        add_payload = {
            "quantity": 2,
            "inventory_id": 5
        }

        response = self.client.post('/servicetickets/1/add-part', json=add_payload)

        self.assertEqual(response.status_code, 201)

