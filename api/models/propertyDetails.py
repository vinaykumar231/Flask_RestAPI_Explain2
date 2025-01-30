
import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from database import db
from sqlalchemy.orm import relationship


# 'P123', 1000000, 5000, 10, '10A', 'East Wing', '2 slots', 'Spacious and well-lit', '2025-01-06', 1

class Property_Detils(db.Model):
    __tablename__ = "property_details"
    id = Column(Integer, primary_key=True, index=True)
    property_code = Column(Integer, ForeignKey("property.property_code"))
    property_image_Path = Column(String(250))
    rate_buy = Column(Float)
    rate_lease = Column(Float)
    floor = Column(Integer)
    unit_no = Column(String(50))
    wing = Column(String(50))
    car_parking = Column(String(50))
    remarks = Column(Text)
    edit_date = Column(DateTime)  # Correct usage
    user_id = Column(Integer, ForeignKey("users.user_id"))

   
    property = relationship("Property", backref="property_details")
    user = relationship("User", backref="property_details")
    

