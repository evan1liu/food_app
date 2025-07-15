import os
import json
import re
import base64
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from get_prompt_for_meal_plan_groceries import get_prompt_for_meal_plan_groceries
from models import OnboardingRequest
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

onboarding_router = APIRouter()

# JSON data loading remains the same...
with open(os.path.join('onboarding_data', 'nutrition_goals.json'), 'r') as f:
    nutrition_goals: list[str] = json.load(f)

with open(os.path.join('onboarding_data', 'allergies.json'), 'r') as f:
    allergies: list[str] = json.load(f)

with open(os.path.join('onboarding_data', 'food_restrictions.json'), 'r') as f:
    food_restrictions: dict[str, list[str]] = json.load(f)

with open(os.path.join('onboarding_data', 'food_preferences.json'), 'r') as f:
    food_preferences: dict[str, list[str]] = json.load(f)

async def generate_meal_image(meal_name: str, meal_index: int) -> Dict[str, Optional[str]]:
    """
    Generate an image for a meal using Gemini.
    """
    try:
        print(f"Generating image for meal {meal_index + 1}: {meal_name}")

        # Create a descriptive prompt for food image generation
        prompt = f"Create a high-quality, appetizing photo of {meal_name}. The image should be well-lit, professionally styled, and show the dish as if it was prepared in a home kitchen. Make it look delicious and appealing. Style: food photography, clean composition."

        # Use Gemini Pro Vision model
        model = genai.GenerativeModel('gemini-pro-vision')
        
        # Generate the image
        response = await asyncio.to_thread(
            model.generate_content,
            prompt
        )

        # Check if we got a response
        if response and hasattr(response, 'parts'):
            # Get the first image part
            for part in response.parts:
                if hasattr(part, 'image_bytes'):
                    image_bytes = part.image_bytes
                    break
            else:
                print(f"No image data found in response for meal {meal_index + 1}: {meal_name}")
                return {"image_url": None, "error": "No image data in response"}

            # Create images directory
            images_dir = os.path.join('backend', 'images')
            os.makedirs(images_dir, exist_ok=True)

            # Create a safe filename
            safe_meal_name = "".join(c for c in meal_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_meal_name = safe_meal_name.replace(' ', '_').lower()
            image_filename = f"meal_{meal_index + 1}_{safe_meal_name}.png"
            image_path = os.path.join(images_dir, image_filename)

            # Save the image data to file
            with open(image_path, 'wb') as f:
                f.write(image_bytes)

            # Return URL path for frontend use
            image_url = f"/images/{image_filename}"
            print(f"Successfully generated and saved image for meal {meal_index + 1}: {meal_name} -> {image_url}")

            return {
                "image_url": image_url,
                "error": None
            }

        print(f"No valid response for meal {meal_index + 1}: {meal_name}")
        return {"image_url": None, "error": "No valid response from model"}

    except Exception as e:
        error_msg = f"Failed to generate image for {meal_name}: {str(e)}"
        print(error_msg)
        return {"image_url": None, "error": error_msg}

async def generate_images_for_meals(meal_plan: List[Dict]) -> List[Dict]:
    """
    Generate images for all meals concurrently.

    Args:
        meal_plan: List of meal dictionaries

    Returns:
        List of meal dictionaries with image_url added
    """
    print(f"Starting concurrent image generation for {len(meal_plan)} meals...")

    # Create tasks for concurrent image generation
    tasks = []
    for i, meal in enumerate(meal_plan):
        task = generate_meal_image(meal.get("meal_name", f"Meal {i+1}"), i)
        tasks.append(task)

    # Wait for all image generation tasks to complete
    image_results = await asyncio.gather(*tasks, return_exceptions=True)

    # Add image data to meals
    updated_meals = []
    for i, (meal, image_result) in enumerate(zip(meal_plan, image_results)):
        updated_meal = meal.copy()

        if isinstance(image_result, Exception):
            print(f"Exception occurred for meal {i+1}: {str(image_result)}")
            updated_meal["image_url"] = None
            updated_meal["image_error"] = str(image_result)
        else:
            updated_meal["image_url"] = image_result.get("image_url")
            if image_result.get("error"):
                updated_meal["image_error"] = image_result["error"]

        updated_meals.append(updated_meal)

    successful_images = sum(1 for meal in updated_meals if meal.get("image_url") is not None)
    print(f"Image generation completed: {successful_images}/{len(meal_plan)} images generated successfully")

    return updated_meals

def parse_llm_response_and_save(response_text: str, user_id: str = "default", meal_plan_with_images: Optional[List[Dict]] = None) -> dict:
    """
    Parse the LLM response to extract meal plan and groceries from XML tags
    and save them to JSON files in the users_data folder.

    Args:
        response_text: The raw response text from the LLM containing XML tags
        user_id: Optional user identifier for file naming (defaults to "default")
        meal_plan_with_images: Optional meal plan data with images already generated

    Returns:
        dict: Contains the parsed meal_plan and groceries data

    Raises:
        HTTPException: If parsing fails or required sections are missing
    """
    try:
        # Extract meal plan from <meal> tags (only if not provided with images)
        if meal_plan_with_images is None:
            meal_pattern = r'<meal>\s*(.*?)\s*</meal>'
            meal_match = re.search(meal_pattern, response_text, re.DOTALL)

            if not meal_match:
                raise HTTPException(status_code=500, detail="No meal plan section found in LLM response")

            meal_json_str = meal_match.group(1).strip()
            # It's safer to load JSON after cleaning up potential markdown formatting
            meal_json_str = re.sub(r'^```json\s*|\s*```$', '', meal_json_str, flags=re.MULTILINE)
            meal_plan = json.loads(meal_json_str)
        else:
            meal_plan = meal_plan_with_images

        # Extract groceries from <groceries> tags
        groceries_pattern = r'<groceries>\s*(.*?)\s*</groceries>'
        groceries_match = re.search(groceries_pattern, response_text, re.DOTALL)
        if not groceries_match:
            raise HTTPException(status_code=500, detail="No groceries found in LLM response")

        groceries_json_str = groceries_match.group(1).strip()
        groceries_json_str = re.sub(r'^```json\s*|\s*```$', '', groceries_json_str, flags=re.MULTILINE)
        groceries = json.loads(groceries_json_str)

        # File paths
        user_data_dir = os.path.join('backend', 'users_data')
        os.makedirs(user_data_dir, exist_ok=True)
        meal_plan_path = os.path.join(user_data_dir, 'meal_plan.json')
        groceries_path = os.path.join(user_data_dir, 'groceries.json')

        # Save to files
        with open(meal_plan_path, 'w') as f:
            json.dump(meal_plan, f, indent=4)
        with open(groceries_path, 'w') as f:
            json.dump(groceries, f, indent=4)

        return {
            "meal_plan": meal_plan,
            "groceries": groceries,
            "files_saved": [meal_plan_path, groceries_path]
        }
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse JSON from LLM response: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred during parsing: {str(e)}")


@onboarding_router.get("/nutrition_goals")
async def get_nutrition_goals():
    return nutrition_goals

@onboarding_router.get("/allergies")
async def get_allergies():
    return allergies

@onboarding_router.get("/food_restrictions")
async def get_food_restrictions():
    return food_restrictions
    
@onboarding_router.get("/food_preferences")
async def get_food_preferences():
    return food_preferences

@onboarding_router.post("/submit_onboarding")
async def submit_onboarding(onboarding_data: OnboardingRequest):
    try:
        prompt = get_prompt_for_meal_plan_groceries(onboarding_data)
        print(prompt)

        # Generate meal plan and groceries with text generation model
        model = genai.GenerativeModel("gemini-1.5-flash")  # Updated model name
        response = await asyncio.to_thread(
            model.generate_content,
            prompt
        )

        # Get the response text
        response_text = response.text
        print(response_text)

        # First, parse the response to get the basic meal plan
        parsed_data = parse_llm_response_and_save(response_text)

        # Generate images for all meals concurrently
        print("Starting image generation for meals...")
        meal_plan_with_images = await generate_images_for_meals(parsed_data["meal_plan"])

        # Save the updated meal plan with images
        meal_plan_with_images_data = parse_llm_response_and_save(
            response_text,
            meal_plan_with_images=meal_plan_with_images
        )

        # Count successful image generations
        successful_images = sum(1 for meal in meal_plan_with_images if meal.get("image_url") is not None)

        return {
            "message": "Onboarding data processed successfully",
            "meal_plan_count": len(meal_plan_with_images_data["meal_plan"]),
            "groceries_count": len(meal_plan_with_images_data["groceries"]),
            "images_generated": successful_images,
            "files_saved": meal_plan_with_images_data["files_saved"]
        }

    except Exception as e:
        print(f"Error in submit_onboarding: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing onboarding request: {str(e)}")
