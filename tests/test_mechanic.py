from app import create_app
from app.models import db, Mechanic
from app.utils.utils import encode_token
import unittest


class TestMechanic(unittest.TestCase):


    def setUp(self):
        self.app = create_app("TestingConfig")
        self.mechanic = Mechanic(
            name='test_mechanic', 
            email='testmechanic@email.com', 
            password='test213', 
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


