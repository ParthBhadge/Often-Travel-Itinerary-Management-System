from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.itineraries import router as itineraries_router
from app.routes.recommendations import router as recommendations_router
from sqlalchemy import create_engine, text  # Import `text` for raw SQL queries
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import sys
# new commit final

# Load environment variables
load_dotenv()

# Get the database URL from the .env file
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to test the database connection
def test_connection():
    try:
        # Test the connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))  # Use `text` for the query
            print("Database connection successful:", result.scalar())
    except Exception as e:
        print("Database connection failed:", str(e))

# Call the test function
test_connection()

# Print Python module search path
print("Python module search path:", sys.path)

# Create the FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (or specify frontend URL)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers for itineraries and recommendations
app.include_router(itineraries_router, prefix="/itineraries")
app.include_router(recommendations_router, prefix="/recommendations")