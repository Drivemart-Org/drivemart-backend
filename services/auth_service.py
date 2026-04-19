from sqlalchemy.orm import Session
import models
from core.security import get_password_hash, verify_password, create_access_token
import httpx

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, name: str, email: str, password: str):
        user = self.db.query(models.User).filter(models.User.email == email).first()
        if user:
            return None, "Email already registered"
            
        hashed_pwd = get_password_hash(password)
        new_user = models.User(email=email, name=name, hashed_password=hashed_pwd)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        
        token = create_access_token(data={"sub": str(new_user.id)})
        return token, None

    def login(self, email: str, password: str):
        user = self.db.query(models.User).filter(models.User.email == email).first()
        if not user or not user.hashed_password or not verify_password(password, user.hashed_password):
            return None, "Incorrect email or password"
            
        token = create_access_token(data={"sub": str(user.id)})
        return token, None

    def google_login(self, credential: str):
        with httpx.Client() as client:
            r = client.get("https://www.googleapis.com/oauth2/v3/userinfo", headers={"Authorization": f"Bearer {credential}"})
            
        if r.status_code != 200:
            return None, "Invalid Google token"
        
        idinfo = r.json()
        email = idinfo.get("email")
        google_id = idinfo.get("sub")
        name = idinfo.get("name")
        
        if not email:
            return None, "Google account has no email"
            
        user = self.db.query(models.User).filter(models.User.email == email).first()
        if not user:
            user = models.User(email=email, name=name, google_provider_id=google_id)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        elif not user.google_provider_id:
            user.google_provider_id = google_id
            self.db.commit()
            
        token = create_access_token(data={"sub": str(user.id)})
        return token, None

    def get_user_by_id(self, user_id: str):
        return self.db.query(models.User).filter(models.User.id == user_id).first()
