from fastapi import APIRouter

from onboarding_routes import onboarding_router
from home_routes import home_router

api_router = APIRouter()

api_router.include_router(onboarding_router, prefix="/onboarding")
api_router.include_router(home_router, prefix="/home")