import os
import json
from fastapi import APIRouter

home_router = APIRouter()

@home_router.get("/meal_plan")
async def get_meal_plan():
    # Read the file dynamically on each request to get the latest data
    with open(os.path.join('backend', 'users_data', 'meal_plan.json'), 'r') as f:
        meal_plan: list[dict[str, any]] = json.load(f)
    return meal_plan
    
@home_router.get("/groceries")
async def get_groceries():
    # Read the file dynamically on each request to get the latest data
    with open(os.path.join('backend', 'users_data', 'groceries.json'), 'r') as f:
        groceries: list[dict[str, any]] = json.load(f)
    return groceries