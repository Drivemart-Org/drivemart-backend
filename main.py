from fastapi import FastAPI
from api import auth, listings, dealers, upload, payments

app = FastAPI(
    title="DriveMart API",
    description="Backend API for DriveMart Phase 1",
    version="1.0.0"
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(listings.router, prefix="/api/v1/listings", tags=["Listings"])
app.include_router(dealers.router, prefix="/api/v1/dealers", tags=["Dealers"])
app.include_router(upload.router, prefix="/api/v1/upload", tags=["Uploads"])
app.include_router(payments.router, prefix="/api/v1/payments", tags=["Payments"])

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def health():
    return {"status": "Welcome to DriveMart API"}
