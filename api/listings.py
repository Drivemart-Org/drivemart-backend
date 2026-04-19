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

@router.get("/{listing_id}", response_model=schemas.ListingDetailResponse)
def get_listing_detail(listing_id: str, db: Session = Depends(get_db)):
    service = ListingService(db)
    listing_data = service.get_listing_detail(listing_id)
    if not listing_data:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing_data
