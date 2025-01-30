from flask import Blueprint, request, jsonify
from api.models.propertyDetails import Property_Detils, db
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename
import os
import uuid
import shutil

# Create the Blueprint for Property Details API
property_details_bp = Blueprint("property_details", __name__)


# Configuration for file uploads
UPLOAD_FOLDER = "static/images"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Function to check allowed file types
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to save uploaded file
def save_upload_file(upload_file):
    if not upload_file or not allowed_file(upload_file.filename):
        return None
    
    try:
        # Ensure a secure filename
        filename = secure_filename(upload_file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

        # Create directories if they don't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Save file correctly
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.stream, buffer)

        # Return relative file path for storing in the database
        return file_path.replace("\\", "/")  # Normalize path

    except Exception as e:
        print(f"Error saving file: {str(e)}")
        return None


@property_details_bp.route("/property_details", methods=["POST"])
def add_property_details():
    try:
        # Extract form data
        property_code = request.form.get("property_code")
        rate_buy = request.form.get("rate_buy")
        rate_lease = request.form.get("rate_lease")
        floor = request.form.get("floor")
        unit_no = request.form.get("unit_no")
        wing = request.form.get("wing")
        car_parking = request.form.get("car_parking")
        remarks = request.form.get("remarks")
        edit_date = request.form.get("edit_date")
        user_id = request.form.get("user_id")

        # Handle file upload
        image_file = request.files.get("property_image")
        image_path = save_upload_file(image_file) if image_file else None

        # Create a new Property_Detils instance
        property_details = Property_Detils(
            property_code=property_code,
            rate_buy=rate_buy,
            rate_lease=rate_lease,
            floor=floor,
            unit_no=unit_no,
            wing=wing,
            car_parking=car_parking,
            remarks=remarks,
            edit_date=edit_date,
            user_id=user_id,
            property_image_Path=image_path,  # Store image path in the database
        )

        # Add to database
        db.session.add(property_details)
        db.session.commit()

        return jsonify({"message": "Property details added successfully!"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# GET endpoint to fetch all property details
@property_details_bp.route("/property_details", methods=["GET"])
def get_property_details():
    try:
        # Query all property details from the database
        property_details = Property_Detils.query.all()

        # Base URL to serve images (adjust this based on your Flask app configuration)
        base_url = "http://127.0.0.1:8003/"

        # Convert the property details into a list of dictionaries
        property_details_list = [
            {
                "id": pd.id,
                "property_code": pd.property_code,
                "rate_buy": pd.rate_buy,
                "rate_lease": pd.rate_lease,
                "floor": pd.floor,
                "unit_no": pd.unit_no,
                "wing": pd.wing,
                "car_parking": pd.car_parking,
                "remarks": pd.remarks,
                "edit_date": pd.edit_date,
                "user_id": pd.user_id,
                "property_image_url": f"{base_url}{pd.property_image_Path}",  # Generate the full URL for the image
            }
            for pd in property_details
        ]

        return jsonify({"property_details": property_details_list}), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400
