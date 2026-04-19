from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class ListingCreateRequest(BaseModel):
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
    description: Optional[str] = None
    photos: Optional[List[str]] = None

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
    dealer: Optional['DealerProfileResponse'] = None
    
    class Config:
        from_attributes = True

class DealerProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    dealership_name: str
    logo_url: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class ListingDetailResponse(ListingResponse):
    description: Optional[str] = None
    features: Optional[Dict[str, Any]] = None
    dealer: Optional[DealerProfileResponse] = None

class SearchResponse(BaseModel):
    items: List[ListingResponse]
    total: int

class DealerMetadataResponse(BaseModel):
    dealer: DealerProfileResponse
    listings: List[ListingResponse]
