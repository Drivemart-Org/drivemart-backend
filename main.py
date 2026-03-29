from fastapi import FastAPI
from api import auth

app = FastAPI(
    title="DriveMart API",
    description="Backend API for DriveMart Phase 1",
    version="1.0.0"
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}
