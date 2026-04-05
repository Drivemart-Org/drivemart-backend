from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class ListingResponse(BaseModel):
    id: UUID
    seller_id: Optional[UUID] = None
    make: str
    model: str
    variant: Optional[str] = None
    year: int
    mileage_km: int
    fuel_type: str
    transmission: str
    asking_price: int
    city: str
    locality: Optional[str] = None
    photos: Optional[List[str]] = None
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class SearchResponse(BaseModel):
    items: List[ListingResponse]
    total: int
