import os
import json
from fastapi import APIRouter

onboarding_router = APIRouter()

with open(os.path.join('backend', 'onboarding_data', 'nutrition_goals.json'), 'r') as f:
    nutrition_goals: list[str] = json.load(f)
    
with open(os.path.join('backend', 'onboarding_data', 'allergies.json'), 'r') as f:
    allergies: list[str] = json.load(f)

    
with open(os.path.join('backend', 'onboarding_data', 'food_restrictions.json'), 'r') as f:
    food_restrictions: dict[str, list[str]] = json.load(f)

@onboarding_router.get("/get_nutrition_goals")
async def get_nutrition_goals():
    return nutrition_goals

@onboarding_router.get("/get_allergies")
async def get_allergies():
    return allergies

@onboarding_router.get("/get_food_restrictions")
async def get_food_restrictions():
    return food_restrictions