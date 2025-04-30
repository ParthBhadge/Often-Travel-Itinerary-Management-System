from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.itinerary import Itinerary
from app.models.day import Day
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Pydantic models for request validation
class DayCreate(BaseModel):
    day_number: int
    hotel: str
    activities: str
    transfers: str

class ItineraryCreate(BaseModel):
    name: str
    region: str
    nights: int
    days: List[DayCreate]

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_itinerary(itinerary: ItineraryCreate, db: Session = Depends(get_db)):
    try:
        # Create the itinerary
        new_itinerary = Itinerary(
            name=itinerary.name,
            region=itinerary.region,
            nights=itinerary.nights,
        )
        db.add(new_itinerary)
        db.commit()
        db.refresh(new_itinerary)

        # Create the associated days
        for day in itinerary.days:
            new_day = Day(
                day_number=day.day_number,
                hotel=day.hotel,
                activities=day.activities,
                transfers=day.transfers,
                itinerary_id=new_itinerary.id,
            )
            db.add(new_day)

        db.commit()
        return {"message": "Itinerary created successfully", "itinerary_id": new_itinerary.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create itinerary: {str(e)}")

@router.get("/")
def get_filtered_itineraries(
    region: str = Query(None, description="Region name"),  # Optional string parameter
    nights: int = Query(None, description="Number of nights"),  # Optional integer parameter
    db: Session = Depends(get_db)
):
    try:
        # Base query for itineraries
        query = db.query(Itinerary)

        # Apply filters if provided
        if region:
            query = query.filter(Itinerary.region.ilike(f"%{region}%"))
        if nights:
            query = query.filter(Itinerary.nights == nights)

        itineraries = query.all()

        # Fetch associated days for each itinerary
        results = []
        for itinerary in itineraries:
            days = db.query(Day).filter(Day.itinerary_id == itinerary.id).all()
            results.append({
                "id": itinerary.id,
                "name": itinerary.name,
                "region": itinerary.region,
                "nights": itinerary.nights,
                "days": [
                    {
                        "day_number": day.day_number,
                        "hotel": day.hotel,
                        "activities": day.activities.split(", "),
                        "transfers": day.transfers.split(", ")
                    } for day in days
                ]
            })

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch itineraries: {str(e)}")