"""main"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.database import Base, engine
from api.v1.auth import router as auth_router

app = FastAPI(title="Courses API")
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    """root"""
    return {
        "message": "Courses API",
        "versions": {
            "v1": "/api/v1"
        },
        "docs": "/docs"
    }