from fastapi import APIRouter
from app.api.v1.endpoints import chords, keys, reharmonization

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(chords.router, prefix="/chords", tags=["chords"])
api_router.include_router(keys.router, prefix="/keys", tags=["keys"])
api_router.include_router(reharmonization.router, prefix="/reharmonize", tags=["reharmonization"])
