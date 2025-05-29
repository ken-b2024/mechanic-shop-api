Auto Shop API

This is a RESTful Flask API for managing a mechanic shop, including customers, mechanics, inventory, and service tickets.

🚀 Features

Customer and mechanic registration and login with JWT tokens

Service ticket creation, assignment to mechanics, and part association

Inventory item CRUD

Role-based authorization using decorators

Rate limiting using Flask-Limiter

Caching for frequently accessed endpoints

Swagger UI documentation

Pagination on selected endpoints (e.g., customers, inventory)

🛠️ Tech Stack

Backend: Flask, SQLAlchemy, Marshmallow

Database: MySQL (Dev), SQLite (Testing)

Caching & Rate Limiting: Flask-Caching, Flask-Limiter

API Documentation: Swagger UI

🧱 Project Structure

app/
├── blueprints/
│   ├── customers.py
│   ├── mechanics.py
│   ├── inventory.py
│   └── service_tickets.py
├── extensions.py
├── models.py
├── schemas.py
├── utils/
│   └── utils.py
config.py
run.py

🔧 Setup

1. Clone the Repository

git clone https://github.com/ken-b2024/mechanic-shop-api.git
cd mechanic-shop-api

2. Create and Activate a Virtual Environment

python -m venv venv
source venv/bin/activate  # on Windows use `venv\Scripts\activate`

3. Install Requirements

pip install -r requirements.txt

4. Configure Environment

Choose one config (DevelopmentConfig, TestingConfig, or ProductionConfig) in create_app():

app = create_app("DevelopmentConfig")

Ensure .env or system environment variables for production:

SQLALCHEMY_DATABASE_URI=<your_prod_db_uri>
SECRET_KEY=<your_secret_key>

5. Run the Application

flask run

📘 API Endpoints

🔑 Authentication

POST /customers/login

POST /mechanics/login

👥 Customers

POST /customers/

GET /customers/?page=1&per_page=10 ✅ Paginated

PUT /customers/ (token required)

DELETE /customers/ (token required)

GET /customers/my-tickets (token required)

🔧 Mechanics

POST /mechanics/

GET /mechanics/

PUT /mechanics/ (token required)

DELETE /mechanics/ (token required)

GET /mechanics/tickets-worked

📝 Service Tickets

POST /servicetickets/

GET /servicetickets/ ❌ Not paginated yet

PUT /servicetickets/<id>

POST /servicetickets/<id>/add-part

📦 Inventory

POST /inventoryitems/

GET /inventoryitems/?page=1&per_page=10 ✅ Paginated

PUT /inventoryitems/<id>

DELETE /inventoryitems/<id>

🛡️ Security

Passwords stored as plaintext (❗️Consider using hashing like bcrypt)

Role-based access enforced via token_required decorator

📈 Rate Limiting

/servicetickets/: 10 requests per hour

/customers/: 5 GETs/hour, 3 PUTs/hour

📦 Caching

GET endpoints for mechanics, customers, and service tickets are cached (180s)

🔪 Testing

Full test suite included (unit and integration tests)

Uses unittest (can be swapped with pytest if preferred)

Switch to TestingConfig in create_app() during tests

Use SQLite in-memory for test DB

Run tests locally:

python -m unittest discover -s tests -p 'test_*.py'

⚙️ CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment.

🔁 CI/CD Stages

Build: Sets up Python and installs dependencies

Test: Runs full test suite

Deploy: Deploys to production on Render after successful tests

🔐 Secrets

Ensure the following secrets are configured in your GitHub repository:

RENDER_API_KEY: Render API key

SERVICE_ID: Render service ID

📄 Workflow File

The CI/CD pipeline is defined in `.github/workflows/ci.yml`, and includes:



- **Build Stage**: Creates a virtual environment, installs dependencies, and prints debug info

- **Test Stage**: Runs the full test suite using `unittest`

- **Deploy Stage**: Deploys to [Render](https://render.com) using secrets



The deployment uses this GitHub Action: [`johnbeynon/render-deploy-action`](https://github.com/johnbeynon/render-deploy-action)

🔮 Future Improvements

Password hashing with bcrypt

Dockerfile and docker-compose setup

Admin panel or frontend dashboard

Pagination and filtering on all list endpoints (e.g., service tickets)

📄 License

MIT

📬 Contact

For questions or contributions, contact [kenneth.brown.2404@gmail.com]

