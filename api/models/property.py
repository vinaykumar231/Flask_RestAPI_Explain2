# api/models/property.py
from sqlalchemy import Column, ForeignKey, Integer, String
from database import db
from sqlalchemy.orm import relationship

class Property(db.Model):
    __tablename__ = "property"
    
    property_code = Column(Integer, primary_key=True,autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    building = Column(String(100), nullable=False)
    address2 = Column(String(255))
    city = Column(String(100))
    area = Column(String(100))
    pin = Column(String(10))
    des_code = Column(String(100))
    lease_code = Column(String(100))
    status_code = Column(String(100))
    usp = Column(String(255))
    company = Column(String(100))
    contact_person1 = Column(String(100))
    contact_person2 = Column(String(100))
    contact_person3 = Column(String(100))
    c_status = Column(String(100))
    property_type = Column(String(100))

    user = relationship("User", backref="properties")
    
