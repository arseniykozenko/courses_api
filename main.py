"""main"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.database import Base, engine
from api.internal.internal import router as internal_router
from api.v1.auth import router as v1_auth_router
from api.v1.users import router as v1_users_router
from api.v1.courses import router as v1_courses_router
from api.v1.enrollments import router as v1_enrollments_router
from api.v2.auth import router as v2_auth_router
from api.v2.users import router as v2_users_router
from api.v2.courses import router as v2_courses_router
from api.v2.enrollments import router as v2_enrollments_router
from middlewares.rate_limit_headers import rate_limit_headers

app = FastAPI(title="Courses API")
Base.metadata.create_all(bind=engine)

app.include_router(internal_router)
app.include_router(v1_auth_router)
app.include_router(v1_users_router)
app.include_router(v1_courses_router)
app.include_router(v1_enrollments_router)
app.include_router(v2_auth_router)
app.include_router(v2_users_router)
app.include_router(v2_courses_router)
app.include_router(v2_enrollments_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(rate_limit_headers)
@app.get("/")
async def root():
    """root"""
    return {
        "message": "Courses API",
        "versions": {
            "internal": "/internal",
            "v1": "/api/v1",
            "v2": "/api/v2",
        },
        "docs": "/docs"
    }