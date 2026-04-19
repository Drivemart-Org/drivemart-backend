from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from api.auth import get_current_user
import models
from services.cloudinary_service import CloudinaryService

router = APIRouter()

@router.post("/")
def upload_image(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image type")
        
    service = CloudinaryService()
    url = service.upload_image(file)
    if not url:
        raise HTTPException(status_code=500, detail="Failed to route image to CDN")
    
    return {"url": url}
