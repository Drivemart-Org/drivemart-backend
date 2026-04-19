from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
import jwt
from config import settings
from services.auth_service import AuthService

router = APIRouter()

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class GoogleLoginRequest(BaseModel):
    credential: str

@router.post("/register", response_model=TokenResponse)
def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    token, error = service.register(user_data.name, user_data.email, user_data.password)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=TokenResponse)
def login(user_data: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    token, error = service.login(user_data.email, user_data.password)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/google", response_model=TokenResponse)
def google_login(req: GoogleLoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    token, error = service.google_login(req.credential)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"access_token": token, "token_type": "bearer"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
        
    service = AuthService(db)
    user = service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.get("/me")
def get_me(current_user: models.User = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "name": current_user.name,
        "role": current_user.role,
        "phone": current_user.phone
    }

@router.post("/otp/send")
def send_otp():
    return {"message": "OTP sent successfully (Simulated)"}

@router.post("/otp/verify")
def verify_otp():
    return {"message": "OTP verified (Simulated)"}
