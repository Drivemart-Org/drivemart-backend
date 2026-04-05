import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User, Listing, DealerProfile, RoleEnum, FuelTypeEnum, TransmissionEnum, ListingStatusEnum

# Ensure tables exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

def seed_db():
    print("Starting database seed...")
    
    # Check if a dummy seller exists, if not create one
    seller = db.query(User).filter(User.email == "dealer@drivemart.com").first()
    if not seller:
        seller = User(
            id=uuid.uuid4(),
            email="dealer@drivemart.com",
            name="Premium Cars Dubai",
            role=RoleEnum.seller,
            is_active=True
        )
        db.add(seller)
        db.commit()
        db.refresh(seller)
        
        # Create dealer profile
        dealer_profile = DealerProfile(
            user_id=seller.id,
            dealership_name="Premium Auto Mart",
            city="Dubai",
            description="Leading premium used car seller."
        )
        db.add(dealer_profile)
        db.commit()
    
    # Check if listings exist
    if db.query(Listing).count() > 0:
        print("Listings already exist. Skipping seed.")
        return

    # Seed Premium Cars
    mock_cars = [
        {
            "make": "Mercedes-Benz",
            "model": "G-Class",
            "variant": "G 63 AMG",
            "year": 2023,
            "mileage_km": 15000,
            "fuel_type": FuelTypeEnum.petrol,
            "transmission": TransmissionEnum.automatic,
            "asking_price": 9500000,
            "city": "Dubai",
            "locality": "Downtown",
            "description": "Pristine G63 AMG with custom interior.",
            "photos": [
                "https://images.unsplash.com/photo-1520031441872-265e4ff70366?auto=format&fit=crop&q=80&w=800",
                "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&q=80&w=800"
            ],
            "status": ListingStatusEnum.active
        },
        {
            "make": "BMW",
            "model": "M5",
            "variant": "Competition",
            "year": 2022,
            "mileage_km": 28000,
            "fuel_type": FuelTypeEnum.petrol,
            "transmission": TransmissionEnum.automatic,
            "asking_price": 12500000,
            "city": "Mumbai",
            "locality": "Bandra",
            "description": "Fastest sedan in the market. Well maintained.",
            "photos": [
                "https://images.unsplash.com/photo-1556189250-93ba2306f021?auto=format&fit=crop&q=80&w=800"
            ],
            "status": ListingStatusEnum.active
        },
        {
            "make": "Toyota",
            "model": "Land Cruiser",
            "variant": "LC300 ZX",
            "year": 2024,
            "mileage_km": 5000,
            "fuel_type": FuelTypeEnum.diesel,
            "transmission": TransmissionEnum.automatic,
            "asking_price": 21000000,
            "city": "Delhi",
            "locality": "Vasant Vihar",
            "description": "Brand new Land Cruiser immediately available.",
            "photos": [
                "https://images.unsplash.com/photo-1590362891991-f776e747a588?auto=format&fit=crop&q=80&w=800"
            ],
            "status": ListingStatusEnum.active
        },
        {
            "make": "Hyundai",
            "model": "Creta",
            "variant": "SX Opt",
            "year": 2023,
            "mileage_km": 12000,
            "fuel_type": FuelTypeEnum.petrol,
            "transmission": TransmissionEnum.automatic,
            "asking_price": 1850000,
            "city": "Pune",
            "locality": "Koregaon Park",
            "description": "Mint condition compact SUV.",
            "photos": [
                "https://images.unsplash.com/photo-1610967399881-b548b87198bb?auto=format&fit=crop&q=80&w=800"
            ],
            "status": ListingStatusEnum.active
        },
        {
            "make": "Mahindra",
            "model": "Thar",
            "variant": "LX 4x4",
            "year": 2021,
            "mileage_km": 35000,
            "fuel_type": FuelTypeEnum.diesel,
            "transmission": TransmissionEnum.automatic,
            "asking_price": 1600000,
            "city": "Bangalore",
            "locality": "Indiranagar",
            "description": "Off-road ready Thar.",
            "photos": [
                "https://images.unsplash.com/photo-1632245889029-e406f0f2cf97?auto=format&fit=crop&q=80&w=800"
            ],
            "status": ListingStatusEnum.active
        }
    ]

    for car in mock_cars:
        listing = Listing(
            seller_id=seller.id,
            make=car["make"],
            model=car["model"],
            variant=car["variant"],
            year=car["year"],
            mileage_km=car["mileage_km"],
            fuel_type=car["fuel_type"],
            transmission=car["transmission"],
            asking_price=car["asking_price"],
            city=car["city"],
            locality=car["locality"],
            description=car["description"],
            photos=car["photos"],
            status=car["status"],
            created_at=datetime.utcnow()
        )
        db.add(listing)

    db.commit()
    print(f"Successfully seeded {len(mock_cars)} listings.")

if __name__ == "__main__":
    seed_db()
