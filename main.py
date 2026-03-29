from fastapi import FastAPI

app = FastAPI(
    title="DriveMart API",
    description="Backend API for DriveMart Phase 1",
    version="1.0.0"
)

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}
