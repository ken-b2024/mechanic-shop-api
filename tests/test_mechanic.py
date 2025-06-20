from app import create_app
from app.models import db, Mechanic
from app.utils.utils import encode_token
import unittest
from app.extensions import bcrypt


class TestMechanic(unittest.TestCase):


    def setUp(self):
        self.app = create_app("TestingConfig")
        hashed_pw = bcrypt.generate_password_hash('test213').decode('utf-8')
        self.mechanic = Mechanic(
            name='test_mechanic', 
            email='testmechanic@email.com', 
            password=hashed_pw, 
            phone='987-654-3210', 
            salary=50000.0
        )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
        self.token = encode_token(1,'admin')
        self.client = self.app.test_client()


    def test_login_mechanic(self):
        credentials = {
            "email": "testmechanic@email.com",
            "password": "test213"
        }

        response = self.client.post('/mechanics/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        return response.json['token']


    def test_invalid_creation(self):
        payload = {
            'name': 'test_mechanic',
            'password': 'test213',
            'phone': '987-654-3210',
            'salary': 50000.0
        }

        response = self.client.post('/mechanics/', json=payload)
        self.assertEqual(response.status_code, 400)


    def test_retrieve_mechanics(self):

        response = self.client.get('/mechanics/')

        self.assertEqual(response.status_code, 200)


    def test_update_mechanic(self):
        update_payload = {
            'name':'David Green', 
            'email':'', 
            # 'password':'', 
            'phone':'', 
            'salary':55000.0
        }
        headers = {'Authorization': 'Bearer ' + self.test_login_mechanic()}

        response = self.client.put('/mechanics/', json=update_payload, headers=headers)

        self.assertEqual(response.status_code, 200)
        data = response.json['Mechanic has been successfully updated']
        self.assertEqual(data['name'], 'David Green')
        self.assertEqual(data['salary'], 55000.0)


    def test_delete_mechanic(self):
        headers =  {'Authorization': 'Bearer ' + self.test_login_mechanic()}

        response = self.client.delete('/mechanics/', headers=headers)

        self.assertEqual(response.status_code, 200)


    def test_tickets_worked(self):

        response = self.client.get('/mechanics/tickets-worked')

        self.assertEqual(response.status_code, 200)
