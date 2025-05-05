from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Day(Base):
    __tablename__ = "days"

    id = Column(Integer, primary_key=True, index=True)
    day_number = Column(Integer, nullable=False)
    hotel = Column(String, nullable=False)
    activities = Column(String, nullable=True)
    transfers = Column(String, nullable=True)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id"))
    itinerary = relationship("Itinerary", back_populates="days")