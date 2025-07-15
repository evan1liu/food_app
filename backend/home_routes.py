import os
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

home_router = APIRouter()

# Define the paths to the data files, assuming the app runs from the project root
USERS_DATA_DIR = os.path.join('backend', 'users_data')
MEAL_PLAN_PATH = os.path.join(USERS_DATA_DIR, 'meal_plan.json')
GROCERIES_PATH = os.path.join(USERS_DATA_DIR, 'groceries.json')

@home_router.get("/meal_plan")
async def get_meal_plan():
    """
    Retrieves the generated meal plan from its JSON file.
    """
    if not os.path.exists(MEAL_PLAN_PATH):
        # Return an empty array if the file doesn't exist, as the frontend expects an array
        return JSONResponse(content=[], status_code=404)
    
    try:
        with open(MEAL_PLAN_PATH, 'r') as f:
            meal_plan_data = json.load(f)
        return JSONResponse(content=meal_plan_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading meal plan file: {str(e)}")

@home_router.get("/groceries")
async def get_groceries():
    """
    Retrieves the generated grocery list from its JSON file.
    """
    if not os.path.exists(GROCERIES_PATH):
        # Return an empty array if the file doesn't exist, as the frontend expects an array
        return JSONResponse(content=[], status_code=404)
    
    try:
        with open(GROCERIES_PATH, 'r') as f:
            groceries_data = json.load(f)
        return JSONResponse(content=groceries_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading groceries file: {str(e)}")
