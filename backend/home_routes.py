import os
import json
from fastapi import APIRouter

home_router = APIRouter()

with open(os.path.join('backend', 'users_data', 'meal_plan.json'), 'r') as f:
    meal_plan: list[dict[str, any]] = json.load(f)

with open(os.path.join('backend', 'users_data', 'groceries.json'), 'r') as f:
    groceries: list[dict[str, any]] = json.load(f)



@home_router.get("/meal_plan")
async def get_meal_plan():
    return meal_plan
    
@home_router.get("/groceries")
async def get_groceries():
    return groceries