from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Itinerary(Base):
    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    region = Column(String, nullable=False)
    nights = Column(Integer, nullable=False)
    days = relationship("Day", back_populates="itinerary")