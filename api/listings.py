from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import schemas
from services.listing_service import ListingService

router = APIRouter()

@router.get("/search", response_model=schemas.SearchResponse)
def search_listings(
    keyword: str = None,
    make: str = None,
    min_price: int = None,
    max_price: int = None,
    sort: str = "date_desc",
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    service = ListingService(db)
    return service.search_listings(keyword, make, min_price, max_price, sort, offset, limit)

from api.auth import get_current_user
import models

@router.get("/me", response_model=schemas.SearchResponse)
def get_my_listings(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    service = ListingService(db)
    items, total = service.get_my_listings(str(current_user.id))
    return {"items": items, "total": total}

@router.get("/{listing_id}", response_model=schemas.ListingDetailResponse)
def get_listing_detail(listing_id: str, db: Session = Depends(get_db)):
    service = ListingService(db)
    listing_data = service.get_listing_detail(listing_id)
    if not listing_data:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing_data

@router.post("/", response_model=schemas.ListingDetailResponse)
def create_listing(
    data: schemas.ListingCreateRequest, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    service = ListingService(db)
    new_listing = service.create_listing(str(current_user.id), data.dict())
    
    listing_data = service.get_listing_detail(str(new_listing.id))
    if not listing_data:
        raise HTTPException(status_code=500, detail="Listing mapping failed")
    return listing_data
