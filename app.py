from flask import Flask, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint
from api.endpoints.property import property_blueprint
from api.endpoints.propertyDetails import property_details_bp
from api.endpoints.user import auth_bp
from database import init_db  # Import your blueprint
from api.models.property import Property, db
from api.models.propertyDetails import Property_Detils



app = Flask(__name__)

migrate = Migrate(app, db)

init_db(app)


SWAGGER_URL = '/swagger'  
API_URL = '/static/swagger.json' 


swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  
    API_URL,  
    config={  
        'app_name': "Flask Property API"
    }
)

# Register Swagger UI blueprint
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Register blueprints (routes)
app.register_blueprint(property_blueprint, url_prefix="/api")
app.register_blueprint(property_details_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api")


# Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create all tables
    app.run(debug=True, host="0.0.0.0", port=8003)
