from flask import Blueprint, request, jsonify
from api.models.property import Property
from auth.auth_bearer import admin_required 
from database import db
from sqlalchemy.orm import joinedload

property_blueprint = Blueprint('property', __name__)



@property_blueprint.route("/properties", methods=["POST"])
@admin_required
def add_property():
    try:
        data = request.get_json()

        # Create a new Property instance using the data received
        new_property = Property(
            #property_code=data['property_code'],
            user_id=data['user_id'],
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
    

@property_blueprint.route("/properties_get_all", methods=["GET"])
def get_properties():
    try:
        # Fetch all properties from the database
        properties = Property.query.options(joinedload(Property.user)).all()
        # If no properties are found, return a message
        if not properties:
            return jsonify({"message": "No properties found"}), 404

        # Serialize the properties list to JSON format
        properties_list = []
        for property in properties:
            properties_list.append({
                "property_code": property.property_code,
                "user_id": property.user_id,
                "user_name": property.user.user_name,
                "building": property.building,
                "address2": property.address2,
                "city": property.city,
                "area": property.area,
                "pin": property.pin,
                "des_code": property.des_code,
                "lease_code": property.lease_code,
                "status_code": property.status_code,
                "usp": property.usp,
                "company": property.company,
                "contact_person1": property.contact_person1,
                "contact_person2": property.contact_person2,
                "contact_person3": property.contact_person3,
                "c_status": property.c_status,
                "property_type": property.property_type
            })

        # Return the list of properties as a JSON response
        return jsonify({"properties": properties_list}), 200

    except Exception as e:
        # In case of any error, return a failure response
        return jsonify({"error": str(e)}), 400
    
@property_blueprint.route("/properties_get_data/<int:property_code>", methods=["GET"])
def get_property_by_id(property_code):
    prop = Property.query.options(joinedload(Property.user)).filter_by(property_code=property_code).first()
    if not prop:
        return jsonify({"error": "Property not found"}), 404

    property_data = {
        "property_code": prop.property_code,
        "user_id": prop.user_id,
        "user_name": prop.user.user_name if prop.user else None,
        "building": prop.building,
        "address2": prop.address2,
        "city": prop.city,
        "area": prop.area,
        "pin": prop.pin,
        "des_code": prop.des_code,
        "lease_code": prop.lease_code,
        "status_code": prop.status_code,
        "usp": prop.usp,
        "company": prop.company,
        "contact_person1": prop.contact_person1,
        "contact_person2": prop.contact_person2,
        "contact_person3": prop.contact_person3,
        "c_status": prop.c_status,
        "property_type": prop.property_type
    }
    return jsonify(property_data), 200


@property_blueprint.route("/properties_update/<int:property_code>", methods=["PUT"])
@admin_required
def update_property(property_code):
    prop = Property.query.filter_by(property_code=property_code).first()

    if not prop:
        return jsonify({"error": "Property not found"}), 404

    try:
        data = request.get_json()

        # Update fields only if the new value is not None
        if data.get("building") is not None:
            prop.building = data["building"]
        if data.get("address2") is not None:
            prop.address2 = data["address2"]
        if data.get("city") is not None:
            prop.city = data["city"]
        if data.get("area") is not None:
            prop.area = data["area"]
        if data.get("pin") is not None:
            prop.pin = data["pin"]
        if data.get("des_code") is not None:
            prop.des_code = data["des_code"]
        if data.get("lease_code") is not None:
            prop.lease_code = data["lease_code"]
        if data.get("status_code") is not None:
            prop.status_code = data["status_code"]
        if data.get("usp") is not None:
            prop.usp = data["usp"]
        if data.get("company") is not None:
            prop.company = data["company"]
        if data.get("contact_person1") is not None:
            prop.contact_person1 = data["contact_person1"]
        if data.get("contact_person2") is not None:
            prop.contact_person2 = data["contact_person2"]
        if data.get("contact_person3") is not None:
            prop.contact_person3 = data["contact_person3"]
        if data.get("c_status") is not None:
            prop.c_status = data["c_status"]
        if data.get("property_type") is not None:
            prop.property_type = data["property_type"]

        db.session.commit()
        return jsonify({"message": "Property updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400



@property_blueprint.route("/properties_delete/<int:property_code>", methods=["DELETE"])
def delete_property(property_code):
    prop = Property.query.filter_by(property_code=property_code).first()

    if not prop:
        return jsonify({"error": "Property not found"}), 404

    try:
        db.session.delete(prop)
        db.session.commit()
        return jsonify({"message": "Property deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400



