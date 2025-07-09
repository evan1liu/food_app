from fastapi import APIRouter

from backend.onboarding_routes import onboarding_router

api_router = APIRouter()

api_router.include_router(onboarding_router, prefix="/onboarding")