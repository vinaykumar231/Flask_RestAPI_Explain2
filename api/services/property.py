from api.models.property import Property, db

def get_all_properties():
    return Property.query.all()

def add_property(data):
    new_property = Property(**data)
    db.session.add(new_property)
    db.session.commit()
    return new_property

def update_property(property_code, data):
    property_item = Property.query.filter_by(property_code=property_code).first()
    if not property_item:
        return None
    for key, value in data.items():
        setattr(property_item, key, value)
    db.session.commit()
    return property_item

def delete_property(property_code):
    property_item = Property.query.filter_by(property_code=property_code).first()
    if property_item:
        db.session.delete(property_item)
        db.session.commit()
        return True
    return False
