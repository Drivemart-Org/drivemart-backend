from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
from core.security import get_password_hash, verify_password, create_access_token
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests

router = APIRouter()

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class GoogleLoginRequest(BaseModel):
    credential: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=TokenResponse)
def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    hashed_pwd = get_password_hash(user_data.password)
    new_user = models.User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    token = create_access_token(data={"sub": str(new_user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=TokenResponse)
def login(user_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if not user or not user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

import httpx

@router.post("/google", response_model=TokenResponse)
def google_login(req: GoogleLoginRequest, db: Session = Depends(get_db)):
    with httpx.Client() as client:
        r = client.get("https://www.googleapis.com/oauth2/v3/userinfo", headers={"Authorization": f"Bearer {req.credential}"})
        
    if r.status_code != 200:
        raise HTTPException(status_code=400, detail="Invalid Google token")
    
    idinfo = r.json()
    email = idinfo.get("email")
    google_id = idinfo.get("sub")
    name = idinfo.get("name")
    
    if not email:
        raise HTTPException(status_code=400, detail="Google account has no email")
        
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        user = models.User(
            email=email,
            name=name,
            google_provider_id=google_id
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    elif not user.google_provider_id:
        user.google_provider_id = google_id
        db.commit()
        
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/otp/send")
def send_otp():
    # Placeholder for SMTP logic
    return {"message": "OTP sent successfully (Simulated)"}

@router.post("/otp/verify")
def verify_otp():
    # Placeholder for OTP verification
    return {"message": "OTP verified (Simulated)"}
