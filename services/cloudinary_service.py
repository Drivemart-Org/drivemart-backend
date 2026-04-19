import cloudinary
import cloudinary.uploader
from fastapi import UploadFile
from config import settings
import uuid

class CloudinaryService:
    def __init__(self):
        if settings.cloudinary_cloud_name and settings.cloudinary_api_key:
            cloudinary.config(
                cloud_name=settings.cloudinary_cloud_name,
                api_key=settings.cloudinary_api_key,
                api_secret=settings.cloudinary_api_secret,
                secure=True
            )
            self.configured = True
        else:
            self.configured = False

    def upload_image(self, file: UploadFile) -> str:
        if not self.configured:
            # Fallback mock URL if Cloudinary is not configured yet in .env
            return f"https://res.cloudinary.com/demo/image/upload/v1612345678/{uuid.uuid4().hex[:8]}.jpg"
            
        try:
            result = cloudinary.uploader.upload(file.file)
            return result.get("secure_url")
        except Exception as e:
            print("Cloudinary Upload Error:", e)
            return None
