import razorpay
from sqlalchemy.orm import Session
import models
from config import settings
import hmac
import hashlib

class PaymentService:
    def __init__(self, db: Session):
        self.db = db
        if settings.razorpay_key_id and settings.razorpay_key_secret:
            self.client = razorpay.Client(auth=(settings.razorpay_key_id, settings.razorpay_key_secret))
        else:
            self.client = None

    def create_order(self, user_id: str, listing_id: str, amount_cents: int) -> dict:
        """Create a Razorpay order and log it as a Transaction."""
        if not self.client:
            raise ValueError("Razorpay is not configured")

        # Amount in paise (e.g. 9900 for 99 AED/INR)
        razorpay_order = self.client.order.create({
            "amount": amount_cents,
            "currency": "INR", # Assuming INR for test, or "AED"
            "payment_capture": "1"
        })

        # Save to DB
        transaction = models.Transaction(
            listing_id=listing_id,
            seller_id=user_id,
            amount=amount_cents,
            razorpay_order_id=razorpay_order['id'],
            status=models.TransactionStatusEnum.created
        )
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)

        return razorpay_order

    def verify_payment(self, razorpay_order_id: str, razorpay_payment_id: str, razorpay_signature: str) -> bool:
        """Verify the razorpay signature and update Transaction/Listing."""
        if not self.client:
            raise ValueError("Razorpay is not configured")

        try:
            self.client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
            
            # If successful, update the transaction and listing
            transaction = self.db.query(models.Transaction).filter(
                models.Transaction.razorpay_order_id == razorpay_order_id
            ).first()

            if transaction:
                transaction.status = models.TransactionStatusEnum.paid
                transaction.razorpay_payment_id = razorpay_payment_id
                
                if transaction.listing_id:
                    listing = self.db.query(models.Listing).filter(
                        models.Listing.id == transaction.listing_id
                    ).first()
                    if listing:
                        listing.is_paid = True
                        listing.status = models.ListingStatusEnum.under_review
                
                self.db.commit()
                return True
                
        except razorpay.errors.SignatureVerificationError:
            return False
            
        return False
