from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from api.deps import get_db
from models import Listing
from typing import Optional
from schemas import SearchResponse

router = APIRouter()

@router.get("/search", response_model=SearchResponse)
def search_listings(
    db: Session = Depends(get_db),
    q: Optional[str] = None,
    make: Optional[str] = None,
    model: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    min_year: Optional[int] = None,
    max_year: Optional[int] = None,
    min_km: Optional[int] = None,
    max_km: Optional[int] = None,
    city: Optional[str] = None,
    sort: Optional[str] = "date_desc",
    status: Optional[str] = "active",
    limit: int = 20,
    offset: int = 0
):
    query = db.query(Listing)

    # 1. Scalable Filter Mapping (Dictionary-driven architecture)
    # This prevents the need for N if-statements. adding a new filter is just 1 line here.
    filter_mapping = {
        "make": lambda v: Listing.make.ilike(f"%{v}%"),
        "model": lambda v: Listing.model.ilike(f"%{v}%"),
        "min_price": lambda v: Listing.asking_price >= v,
        "max_price": lambda v: Listing.asking_price <= v,
        "min_year": lambda v: Listing.year >= v,
        "max_year": lambda v: Listing.year <= v,
        "min_km": lambda v: Listing.mileage_km >= v,
        "max_km": lambda v: Listing.mileage_km <= v,
        "city": lambda v: Listing.city.ilike(f"%{v}%"),
        "status": lambda v: Listing.status == v if v != "all" else None
    }

    # 2. Extract passed parameters
    params = {
        "make": make, "model": model, "min_price": min_price, 
        "max_price": max_price, "min_year": min_year, "max_year": max_year,
        "min_km": min_km, "max_km": max_km, "city": city, "status": status
    }

    # 3. Apply exact and range filters dynamically
    for key, value in params.items():
        if value is not None:
            condition = filter_mapping[key](value)
            if condition is not None:
                query = query.filter(condition)

    # 4. Apply advanced keyword search
    if q:
        search_filter = or_(
            Listing.make.ilike(f"%{q}%"),
            Listing.model.ilike(f"%{q}%"),
            Listing.description.ilike(f"%{q}%"),
            Listing.variant.ilike(f"%{q}%")
        )
        query = query.filter(search_filter)
        
    # 5. Apply advanced sorting
    if sort == "date_asc":
        query = query.order_by(Listing.created_at.asc())
    elif sort == "price_desc":
        query = query.order_by(desc(Listing.asking_price))
    elif sort == "price_asc":
        query = query.order_by(Listing.asking_price.asc())
    elif sort == "km_desc":
        query = query.order_by(desc(Listing.mileage_km))
    elif sort == "km_asc":
        query = query.order_by(Listing.mileage_km.asc())
    elif sort == "year_desc":
        query = query.order_by(desc(Listing.year))
    elif sort == "year_asc":
        query = query.order_by(Listing.year.asc())
    else:
        query = query.order_by(desc(Listing.created_at)) # Default date_desc
    
    total = query.count()
    items = query.offset(offset).limit(limit).all()
    
    return {"items": items, "total": total}
