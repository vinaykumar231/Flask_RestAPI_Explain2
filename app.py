from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint
from api.endpoints.property import property_blueprint
from database import init_db  # Import your blueprint
from api.models.property import Property, db

# Initialize Flask app
app = Flask(__name__)

# Initialize database
init_db(app)

# Swagger UI configuration
SWAGGER_URL = '/swagger'  # URL for Swagger UI
API_URL = '/static/swagger.json'  # Location of Swagger JSON file

# Create Swagger UI blueprint
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI route
    API_URL,  # API documentation URL
    config={  # Swagger UI configuration
        'app_name': "Flask Property API"
    }
)

# Register Swagger UI blueprint
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Register blueprints (routes)
app.register_blueprint(property_blueprint, url_prefix="/api")

# Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create all tables
    app.run(debug=True, host="0.0.0.0", port=8003)
