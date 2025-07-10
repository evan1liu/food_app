import os
import json
from datetime import datetime
from fastapi import APIRouter, HTTPException
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
    return food_preferences  # Changed from {} to food_preferences

class OnboardingRequest(BaseModel):
    time_to_cook_per_day: float
    money_to_spend_per_week: float
    allergies: list[str]
    nutrition_goals: list[str]
    food_restrictions: list[str]
    food_preferences: dict[str, str]
    address: str  # Changed from dict to str to match frontend

def save_onboarding_data(data: dict) -> str:
    """Save onboarding data to JSON file and return the unique ID"""
    # Create submissions directory if it doesn't exist
    submissions_dir = os.path.join('backend', 'submissions')
    os.makedirs(submissions_dir, exist_ok=True)
    
    # Generate unique ID based on timestamp
    submission_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    
    # Add metadata
    submission_data = {
        "id": submission_id,
        "timestamp": datetime.now().isoformat(),
        "data": data
    }
    
    # Save individual submission
    submission_file = os.path.join(submissions_dir, f"{submission_id}.json")
    with open(submission_file, 'w') as f:
        json.dump(submission_data, f, indent=2)
    
    # Also append to master submissions file for easy access
    master_file = os.path.join(submissions_dir, 'all_submissions.json')
    
    # Read existing submissions or create empty list
    try:
        with open(master_file, 'r') as f:
            all_submissions = json.load(f)
    except FileNotFoundError:
        all_submissions = []
    
    # Add new submission
    all_submissions.append(submission_data)
    
    # Save updated master file
    with open(master_file, 'w') as f:
        json.dump(all_submissions, f, indent=2)
    
    return submission_id
    
@onboarding_router.post("/submit_onboarding")  # Changed from GET to POST
async def submit_onboarding(onboarding_data: OnboardingRequest):
    try:
        # Convert to dict for storage
        data_dict = onboarding_data.model_dump()
        
        # Save the data and get the submission ID
        submission_id = save_onboarding_data(data_dict)
        
        return {
            "message": "Onboarding completed successfully", 
            "submission_id": submission_id,
            "data": onboarding_data
        } 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save onboarding data: {str(e)}") 