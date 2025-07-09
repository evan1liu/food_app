import os
import json
from fastapi import APIRouter
from pydantic import BaseModel

onboarding_router = APIRouter()

with open(os.path.join('backend', 'onboarding_data', 'nutrition_goals.json'), 'r') as f:
    nutrition_goals: list[str] = json.load(f)
    
with open(os.path.join('backend', 'onboarding_data', 'allergies.json'), 'r') as f:
    allergies: list[str] = json.load(f)

    
with open(os.path.join('backend', 'onboarding_data', 'food_restrictions.json'), 'r') as f:
    food_restrictions: dict[str, list[str]] = json.load(f)
    
with open(os.path.join('backend', 'onboarding_data', 'food_preferences.json'), 'r') as f:
    food_preferences: dict[str, list[str]] = json.load(f)

@onboarding_router.get("/get_nutrition_goals")
async def get_nutrition_goals():
    return nutrition_goals

@onboarding_router.get("/get_allergies")
async def get_allergies():
    return allergies

@onboarding_router.get("/get_food_restrictions")
async def get_food_restrictions():
    return food_restrictions


@onboarding_router.get("/get_food_preferences")
async def get_food_preferences():
    return {} # Placeholder

class OnboardingRequest(BaseModel):
    time_to_cook_per_day: float
    money_to_spend_per_week: float
    allergies: list[str]
    nutrition_goals: list[str]
    food_restrictions: list[str]
    food_preferences: dict[str, str]
    address: str
    
@onboarding_router.post("/submit_onboarding")  # Changed from GET to POST
async def submit_onboarding(onboarding_data: OnboardingRequest):
    # Process the onboarding data here
    # For example, save to database, generate meal plan, etc.
    return {"message": "Onboarding completed successfully", "data": onboarding_data} 