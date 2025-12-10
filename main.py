"""main"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.database import Base, engine
from api.v1.auth import router as auth_router
from api.v1.users import router as users_router
from api.v1.courses import router as courses_router
from api.v1.enrollments import router as enrollments_router

app = FastAPI(title="Courses API")
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(courses_router)
app.include_router(enrollments_router)

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