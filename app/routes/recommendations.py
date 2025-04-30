from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.itinerary import Itinerary
from app.models.day import Day

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/recommendations")
def get_recommendations(
    nights: int = Query(..., description="Number of nights"),  # Required integer parameter
    region: str = Query(None, description="Region name"),  # Optional string parameter
    db: Session = Depends(get_db)
):
    try:
        print(f"Received query parameters: nights={nights}, region={region}")

        # Fetch itineraries based on nights and region
        query = db.query(Itinerary).filter(Itinerary.nights <= nights)
        if region:
            query = query.filter(Itinerary.region.ilike(f"%{region}%"))
        itineraries = query.all()

        print(f"Fetched itineraries: {itineraries}")

        if not itineraries:
            raise HTTPException(status_code=404, detail="No itineraries found for the given criteria")

        # Fetch associated days for each itinerary
        results = []
        for itinerary in itineraries:
            days = db.query(Day).filter(Day.itinerary_id == itinerary.id).all()
            print(f"Days for itinerary {itinerary.id}: {days}")
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
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch recommendations: {str(e)}")