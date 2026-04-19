from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
import models

class ListingService:
    def __init__(self, db: Session):
        self.db = db

    def search_listings(self, 
        keyword: str = None, make: str = None, 
        min_price: int = None, max_price: int = None,
        sort: str = "date_desc", offset: int = 0, limit: int = 20
    ):
        query = self.db.query(models.Listing).filter(models.Listing.status == models.ListingStatusEnum.active)
        
        if keyword:
            query = query.filter(
                or_(
                    models.Listing.make.ilike(f"%{keyword}%"),
                    models.Listing.model.ilike(f"%{keyword}%"),
                    models.Listing.variant.ilike(f"%{keyword}%")
                )
            )
        if make:
            query = query.filter(models.Listing.make.ilike(f"%{make}%"))
        if min_price:
            query = query.filter(models.Listing.asking_price >= min_price)
        if max_price:
            query = query.filter(models.Listing.asking_price <= max_price)
            
        sort_options = {
            "date_desc": desc(models.Listing.created_at),
            "date_asc": models.Listing.created_at,
            "price_desc": desc(models.Listing.asking_price),
            "price_asc": models.Listing.asking_price,
            "km_desc": desc(models.Listing.mileage_km),
            "km_asc": models.Listing.mileage_km,
            "year_desc": desc(models.Listing.year),
            "year_asc": models.Listing.year
        }
        
        query = query.order_by(sort_options.get(sort, desc(models.Listing.created_at)))
        total = query.count()
        items = query.offset(offset).limit(limit).all()
        
        seller_ids = [item.seller_id for item in items if item.seller_id]
        dealers = self.db.query(models.DealerProfile).filter(models.DealerProfile.user_id.in_(seller_ids)).all() if seller_ids else []
        dealer_map = {d.user_id: d for d in dealers}
        
        result_items = []
        for item in items:
            data = item.__dict__.copy()
            if item.seller_id and item.seller_id in dealer_map:
                data['dealer'] = dealer_map[item.seller_id]
            result_items.append(data)
            
        return {"items": result_items, "total": total}

    def get_listing_detail(self, listing_id: str):
        listing = self.db.query(models.Listing).filter(models.Listing.id == listing_id).first()
        if not listing:
            return None
            
        dealer = None
        if listing.seller_id:
            dealer = self.db.query(models.DealerProfile).filter(models.DealerProfile.user_id == listing.seller_id).first()
            
        listing_data = listing.__dict__.copy()
        if dealer:
            listing_data["dealer"] = dealer
            
        return listing_data
