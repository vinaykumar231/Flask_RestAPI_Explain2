from flask import Blueprint, request, jsonify
from api.models.propertyDetails import Property_Detils, db
from sqlalchemy.exc import SQLAlchemyError

# Create the Blueprint for Property Details API
property_details_bp = Blueprint("property_details", __name__)

# POST endpoint to create property details
@property_details_bp.route("/property_details", methods=["POST"])
def add_property_details():
    try:
        # Get data from request
        data = request.get_json()

        # Create a new Property_Detils instance
        property_details = Property_Detils(
            property_code=data["property_code"],
            rate_buy=data["rate_buy"],
            rate_lease=data["rate_lease"],
            floor=data["floor"],
            unit_no=data["unit_no"],
            wing=data["wing"],
            car_parking=data["car_parking"],
            remarks=data["remarks"],
            edit_date=data.get("edit_date"),  # Optional field
            user_id=data["user_id"],
        )

        # Add the new property details to the database
        db.session.add(property_details)
        db.session.commit()

        return jsonify({"message": "Property details added successfully!"}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# GET endpoint to fetch all property details
@property_details_bp.route("/property_details", methods=["GET"])
def get_property_details():
    try:
        # Query all property details from the database
        property_details = Property_Detils.query.all()

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
            }
            for pd in property_details
        ]

        return jsonify({"property_details": property_details_list}), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400
