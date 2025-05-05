from app.database import SessionLocal, engine
from app.models.itinerary import Itinerary
from app.models.day import Day
from app.database import Base

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Sample Itinerary for Phuket
# phuket_itinerary = Itinerary(name="Phuket 3 Nights", region="Phuket", nights=3)
# phuket_days = [
#     Day(day_number=1, hotel="Phuket Beach Resort", activities="Visit Patong Beach, Explore Bangla Road", transfers="Airport to Hotel", itinerary=phuket_itinerary),
#     Day(day_number=2, hotel="Phuket Beach Resort", activities="Phi Phi Islands Tour, Snorkeling", transfers="Hotel to Pier, Pier to Hotel", itinerary=phuket_itinerary),
#     Day(day_number=3, hotel="Phuket Beach Resort", activities="Relax at Kata Beach", transfers="Hotel to Airport", itinerary=phuket_itinerary),
# ]

# db.add(phuket_itinerary)
# db.add_all(phuket_days)
# db.commit()
# db.close()