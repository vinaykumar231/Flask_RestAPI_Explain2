from flask import Blueprint, request, jsonify
from api.models.property import Property
from database import db

property_blueprint = Blueprint('property', __name__)

@property_blueprint.route("/properties", methods=["POST"])
def add_property():
    try:
        # Parse JSON data from the request
        data = request.get_json()

        # Create a new Property instance using the data received
        new_property = Property(
            property_code=data['property_code'],
            building=data['building'],
            address2=data.get('address2', ''),
            city=data.get('city', ''),
            area=data.get('area', ''),
            pin=data.get('pin', ''),
            des_code=data.get('des_code', ''),
            lease_code=data.get('lease_code', ''),
            status_code=data.get('status_code', ''),
            usp=data.get('usp', ''),
            company=data.get('company', ''),
            contact_person1=data.get('contact_person1', ''),
            contact_person2=data.get('contact_person2', ''),
            contact_person3=data.get('contact_person3', ''),
            c_status=data.get('c_status', ''),
            property_type=data.get('property_type', '')
        )

        # Add the new property to the session and commit
        db.session.add(new_property)
        db.session.commit()

        # Return a success response
        return jsonify({"message": "Property added successfully", "property_code": new_property.property_code}), 201

    except Exception as e:
        # In case of any error, return a failure response
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
