from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import schemas
from services.dealer_service import DealerService

router = APIRouter()

@router.get("/{dealer_id}", response_model=schemas.DealerMetadataResponse)
def get_dealer_profile(dealer_id: str, db: Session = Depends(get_db)):
    service = DealerService(db)
    result = service.get_dealer_profile(dealer_id)
    if not result:
        raise HTTPException(status_code=404, detail="Dealer not found")
    return result
