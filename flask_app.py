from app import create_app
from app.models import db

app = create_app('ProductionConfig')

with app.app_context():
    # db.drop_all()
    db.create_all()

@app.route('/')
def home():
    return "<h1>Welcome to the Mechanic Shop API Database!<h1>"

