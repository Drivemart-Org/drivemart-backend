from sqlalchemy.orm import Session
from sqlalchemy import desc
import models

class DealerService:
    def __init__(self, db: Session):
        self.db = db

    def get_dealer_profile(self, dealer_id: str):
        dealer = self.db.query(models.DealerProfile).filter(models.DealerProfile.id == dealer_id).first()
        if not dealer:
            return None
            
        listings = self.db.query(models.Listing).filter(
            models.Listing.seller_id == dealer.user_id, 
            models.Listing.status == models.ListingStatusEnum.active
        ).order_by(desc(models.Listing.created_at)).all()
        
        return {
            "dealer": dealer,
            "listings": listings
        }
