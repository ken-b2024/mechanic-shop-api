from app import create_app
from app.models import db, Inventory
import unittest


class TestInventory(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.inventory_item = Inventory(
            name = 'Engine oil',
            price = 89.99
        )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.inventory_item)
            db.session.commit()
        self.client = self.app.test_client()


    def test_create_inventory_item(self):
        payload = {
            'name': 'Engine oil',
            'price': 89.99
        }

        response = self.client.post('/inventoryitems/', json=payload)

        self.assertEqual(response.status_code, 201)


    def test_retrieve_items(self):

        response = self.client.get('/inventoryitems/')

        self.assertEqual(response.status_code, 200)


    def test_invalid_update(self):
        udpate_payload = {
            'price': 98.99
        }

        response = self.client.put('/inventoryitems/1', json=udpate_payload)

        self.assertEqual(response.status_code, 400)


    def test_delete_inventory_item(self):

        response = self.client.delete('/inventoryitems/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Successfully deleted inventory item with ID: 1')
