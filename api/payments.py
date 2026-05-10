from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import schemas
from services.payment_service import PaymentService
from api.auth import get_current_user
import models

router = APIRouter(tags=["payments"])

@router.post("/create-order", response_model=schemas.PaymentOrderResponse)
def create_order(
    request: schemas.PaymentOrderCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    payment_service = PaymentService(db)
    
    # We set a fixed amount for listing fee: e.g. 9900 paise (99 INR)
    listing_fee_amount = 9900 
    
    try:
        order = payment_service.create_order(
            user_id=current_user.id,
            listing_id=str(request.listing_id),
            amount_cents=listing_fee_amount
        )
        return schemas.PaymentOrderResponse(
            razorpay_order_id=order["id"],
            amount=order["amount"],
            currency=order["currency"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/verify")
def verify_payment(
    request: schemas.PaymentVerifyRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    payment_service = PaymentService(db)
    
    is_valid = payment_service.verify_payment(
        razorpay_order_id=request.razorpay_order_id,
        razorpay_payment_id=request.razorpay_payment_id,
        razorpay_signature=request.razorpay_signature
    )
    
    if not is_valid:
        raise HTTPException(status_code=400, detail="Payment signature verification failed")
        
    return {"status": "success", "message": "Payment verified successfully"}
