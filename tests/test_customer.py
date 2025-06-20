from app import create_app
from app.models import db, Customer
from app.utils.utils import encode_token
import unittest
from app.extensions import bcrypt


class TestCustomer(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        hashed_pw = bcrypt.generate_password_hash('test321').decode('utf-8')
        self.customer = Customer(name='test_user', email='testuser@email.com', password=hashed_pw, phone='123-456-7890', make_model='Lexus RX 350', VIN='2T2HZMDA1PC123456')

        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
            
        self.token = encode_token(1,'admin')
        self.client = self.app.test_client()


    def test_create_customer(self):
        customer_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
           	"password": "1jd0!",
            "phone": "313-646-5585",
            "make_model": "Hyundai Tuscan",
            "VIN": "KM8J3CA46MU123456"
        }

        response = self.client.post('/customers/', json=customer_payload)
        # print(response.status_code)
        # print(response.get_json()) 
        self.assertEqual(response.status_code, 201)
        data = response.get_json()["New customer has been created successfully"]
        self.assertEqual(data['name'], "John Doe")


    def test_invalid_creation(self):
        customer_payload = {
            "name": "John Doe",
            "phone": "123-456-7890",
            "password": "123" 
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field.'])


    def test_login_customer(self):
        credentials = {
            "email": "testuser@email.com",
            "password": "test321"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        return response.json['token']


    def test_invalid_login(self):
        credentials = {
            "email": "bad_email@email.com",
            "password": "bad_pw"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Invalid email or password!')


    def test_update_customer(self):
        udpate_payload = {
            "name": "",
            "email": "",
           	"password": "",
            "phone": "",
            "make_model": "",
            "VIN": "2T2HZMDA1PC123789"
        }

        headers = {'Authorization': 'Bearer ' + self.test_login_customer()}

        response = self.client.put('/customers/', json=udpate_payload, headers=headers)

        self.assertEqual(response.status_code, 200)
        updated_customer = response.json["Customer has been successfully updated"]
        self.assertEqual(updated_customer['VIN'], '2T2HZMDA1PC123789')
    
    
    def test_invalid_update(self):
        udpate_payload = {
            "name": "",
            "email": "",
           	"password": "",
            "phone": "",
            "make_model": ""
        }

        headers = {'Authorization': 'Bearer ' + self.test_login_customer()}

        response = self.client.put('/customers/', json=udpate_payload, headers=headers)

        self.assertEqual(response.status_code, 400)


    def test_retrieve_customers(self):

        response = self.client.get('/customers/')

        self.assertEqual(response.status_code, 200)



    def test_delete_customer(self):
        headers = {'Authorization': 'Bearer ' + self.test_login_customer()}

        response = self.client.delete('/customers/', headers=headers)

        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Successfully deleted customer with ID: 1')

