import os
import json
import re
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.get_prompt_for_meal_plan_groceries import get_prompt_for_meal_plan_groceries
from backend.models import OnboardingRequest
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()


onboarding_router = APIRouter()

with open(os.path.join('backend', 'onboarding_data', 'nutrition_goals.json'), 'r') as f:
    nutrition_goals: list[str] = json.load(f)
    
with open(os.path.join('backend', 'onboarding_data', 'allergies.json'), 'r') as f:
    allergies: list[str] = json.load(f)

    
with open(os.path.join('backend', 'onboarding_data', 'food_restrictions.json'), 'r') as f:
    food_restrictions: dict[str, list[str]] = json.load(f)
    
with open(os.path.join('backend', 'onboarding_data', 'food_preferences.json'), 'r') as f:
    food_preferences: dict[str, list[str]] = json.load(f)

def parse_llm_response_and_save(response_text: str, user_id: str = "default") -> dict:
    """
    Parse the LLM response to extract meal plan and groceries from XML tags
    and save them to JSON files in the users_data folder.
    
    Args:
        response_text: The raw response text from the LLM containing XML tags
        user_id: Optional user identifier for file naming (defaults to "default")
        
    Returns:
        dict: Contains the parsed meal_plan and groceries data
        
    Raises:
        HTTPException: If parsing fails or required sections are missing
    """
    try:
        # Extract meal plan from <meal> tags
        meal_pattern = r'<meal>\s*(.*?)\s*</meal>'
        meal_match = re.search(meal_pattern, response_text, re.DOTALL)
        
        if not meal_match:
            raise HTTPException(status_code=500, detail="No meal plan section found in LLM response")
        
        meal_json_str = meal_match.group(1).strip()
        meal_plan = json.loads(meal_json_str)
        
        # Extract groceries from <groceries> tags
        groceries_pattern = r'<groceries>\s*(.*?)\s*</groceries>'
        groceries_match = re.search(groceries_pattern, response_text, re.DOTALL)
        
        if not groceries_match:
            raise HTTPException(status_code=500, detail="No groceries section found in LLM response")
        
        groceries_json_str = groceries_match.group(1).strip()
        groceries = json.loads(groceries_json_str)
        
        # Ensure users_data directory exists
        users_data_dir = os.path.join('backend', 'users_data')
        os.makedirs(users_data_dir, exist_ok=True)
        
        # Create user-specific subdirectory if using user_id
        if user_id != "default":
            user_dir = os.path.join(users_data_dir, user_id)
            os.makedirs(user_dir, exist_ok=True)
            meal_plan_path = os.path.join(user_dir, 'meal_plan.json')
            groceries_path = os.path.join(user_dir, 'groceries.json')
        else:
            meal_plan_path = os.path.join(users_data_dir, 'meal_plan.json')
            groceries_path = os.path.join(users_data_dir, 'groceries.json')
        
        # Save meal plan to JSON file
        with open(meal_plan_path, 'w') as f:
            json.dump(meal_plan, f, indent=2)
        
        # Save groceries to JSON file
        with open(groceries_path, 'w') as f:
            json.dump(groceries, f, indent=2)
        
        print(f"Meal plan saved to: {meal_plan_path}")
        print(f"Groceries saved to: {groceries_path}")
        
        return {
            "meal_plan": meal_plan,
            "groceries": groceries,
            "files_saved": {
                "meal_plan_path": meal_plan_path,
                "groceries_path": groceries_path
            }
        }
        
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse JSON from LLM response: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing LLM response: {str(e)}")

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
    
@onboarding_router.post("/submit_onboarding")  # Changed from GET to POST
async def submit_onboarding(onboarding_data: OnboardingRequest):
    prompt = get_prompt_for_meal_plan_groceries(onboarding_data)
    print(prompt)
    
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=prompt
    )

    print(response.text)
    
    # Parse the response and save to files
    parsed_data = parse_llm_response_and_save(response.text)
    
    return {
        "message": "Onboarding data processed successfully",
        "meal_plan_count": len(parsed_data["meal_plan"]),
        "groceries_count": len(parsed_data["groceries"]),
        "files_saved": parsed_data["files_saved"]
    }