import os
import json
import re
<<<<<<< Updated upstream
import base64
import asyncio
from typing import Dict, List, Optional
=======
import uuid
>>>>>>> Stashed changes
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.get_prompt_for_meal_plan_groceries import get_prompt_for_meal_plan_groceries
from backend.models import OnboardingRequest
from dotenv import load_dotenv
from google import genai
<<<<<<< Updated upstream
from google.genai import types
from io import BytesIO

load_dotenv()

client = genai.Client()
=======
from PIL import Image
import io


load_dotenv()

# Configure the Gemini client
# Make sure your GOOGLE_API_KEY is set in your .env file
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
>>>>>>> Stashed changes

onboarding_router = APIRouter()

# JSON data loading remains the same...
with open(os.path.join('backend', 'onboarding_data', 'nutrition_goals.json'), 'r') as f:
    nutrition_goals: list[str] = json.load(f)
    
with open(os.path.join('backend', 'onboarding_data', 'allergies.json'), 'r') as f:
    allergies: list[str] = json.load(f)

with open(os.path.join('backend', 'onboarding_data', 'food_restrictions.json'), 'r') as f:
    food_restrictions: dict[str, list[str]] = json.load(f)
    
with open(os.path.join('backend', 'onboarding_data', 'food_preferences.json'), 'r') as f:
    food_preferences: dict[str, list[str]] = json.load(f)

async def generate_meal_image(meal_name: str, meal_index: int) -> Dict[str, Optional[str]]:
    """
    Generate an image for a meal using Imagen 4 with landscape aspect ratio.
    """
    try:
        print(f"Generating image for meal {meal_index + 1}: {meal_name}")
        
        # Create a descriptive prompt for food image generation
        prompt = f"Create a high-quality, appetizing photo of {meal_name}. The image should be well-lit, professionally styled, and show the dish as if it was prepared in a home kitchen. Make it look delicious and appealing. Style: food photography, clean composition."
        
        # Use Imagen 4 with landscape aspect ratio
        response = client.models.generate_images(
            model='imagen-4.0-generate-preview-06-06',
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="4:3"  # Horizontal landscape format
                # Other options: "16:9" for widescreen, "1:1" for square
            )
        )
        
        # Extract image data from response
        if response.generated_images:
            generated_image = response.generated_images[0]
            
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
                f.write(generated_image.image.image_bytes)
            
            # Return URL path for frontend use
            image_url = f"/images/{image_filename}"
            print(f"Successfully generated and saved image for meal {meal_index + 1}: {meal_name} -> {image_url}")
            
            return {
                "image_url": image_url,
                "error": None
            }
        
        print(f"No image data found in response for meal {meal_index + 1}: {meal_name}")
        return {"image_url": None, "error": "No image data in response"}
        
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
<<<<<<< Updated upstream
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
            meal_plan = json.loads(meal_json_str)
        else:
            meal_plan = meal_plan_with_images
        
        # Extract groceries from <groceries> tags
=======
    Parse the LLM response, generate images for each meal, and save all data.
    """
    try:
        # Extract meal plan
        meal_pattern = r'<meal>\s*(.*?)\s*</meal>'
        meal_match = re.search(meal_pattern, response_text, re.DOTALL)
        if not meal_match:
            raise HTTPException(status_code=500, detail="No meal plan found in LLM response")
        meal_plan = json.loads(meal_match.group(1).strip())

        # Extract groceries
>>>>>>> Stashed changes
        groceries_pattern = r'<groceries>\s*(.*?)\s*</groceries>'
        groceries_match = re.search(groceries_pattern, response_text, re.DOTALL)
        if not groceries_match:
            raise HTTPException(status_code=500, detail="No groceries found in LLM response")
        groceries = json.loads(groceries_match.group(1).strip())

        # --- Image Generation ---
        image_model = genai.GenerativeModel('imagen-3') # Using a hypothetical powerful image model
        
        recipe_images_dir = os.path.join('frontend', 'static', 'images', 'recipes')
        os.makedirs(recipe_images_dir, exist_ok=True)

        for meal in meal_plan:
            image_prompt = meal.get("image_prompt")
            if image_prompt:
                try:
                    # Generate the image from the prompt provided by the meal plan
                    image_response = image_model.generate_content(image_prompt)
                    
                    # Assuming the response contains accessible image data
                    if hasattr(image_response, 'media') and image_response.media:
                        image_data = image_response.media[0].data
                        img = Image.open(io.BytesIO(image_data))
                        
                        # Save the image with a unique name
                        image_filename = f"{uuid.uuid4()}.png"
                        image_path = os.path.join(recipe_images_dir, image_filename)
                        img.save(image_path)

                        # Add the relative URL to the meal object for frontend access
                        meal['image_url'] = f"/images/recipes/{image_filename}"
                    else:
                        meal['image_url'] = None # No image was generated
                except Exception as e:
                    print(f"Error generating image for '{meal.get('meal_name')}': {e}")
                    meal['image_url'] = None # Set to null on failure

        # --- Save Data ---
        users_data_dir = os.path.join('backend', 'users_data')
        os.makedirs(users_data_dir, exist_ok=True)
        
        user_dir = os.path.join(users_data_dir, user_id) if user_id != "default" else users_data_dir
        os.makedirs(user_dir, exist_ok=True)

        meal_plan_path = os.path.join(user_dir, 'meal_plan.json')
        groceries_path = os.path.join(user_dir, 'groceries.json')

        with open(meal_plan_path, 'w') as f:
            json.dump(meal_plan, f, indent=2)
        
        with open(groceries_path, 'w') as f:
            json.dump(groceries, f, indent=2)
            
        return {
            "meal_plan": meal_plan,
            "groceries": groceries,
            "files_saved": {"meal_plan_path": meal_plan_path, "groceries_path": groceries_path}
        }
        
    except (json.JSONDecodeError, Exception) as e:
        raise HTTPException(status_code=500, detail=f"Error parsing LLM response or generating images: {str(e)}")

# --- API Endpoints ---
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
    return food_preferences
    
@onboarding_router.post("/submit_onboarding")
async def submit_onboarding(onboarding_data: OnboardingRequest):
<<<<<<< Updated upstream
    try:
        prompt = get_prompt_for_meal_plan_groceries(onboarding_data)
        print(prompt)
        
        # Generate meal plan and groceries with text generation model
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt
        )

        print(response.text)
        
        # First, parse the response to get the basic meal plan
        parsed_data = parse_llm_response_and_save(response.text)
        
        # Generate images for all meals concurrently
        print("Starting image generation for meals...")
        meal_plan_with_images = await generate_images_for_meals(parsed_data["meal_plan"])
        
        # Save the updated meal plan with images
        meal_plan_with_images_data = parse_llm_response_and_save(
            response.text, 
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
=======
    prompt = get_prompt_for_meal_plan_groceries(onboarding_data)
    
    # Use the new text generation model for creating the plan
    text_model = genai.GenerativeModel('gemini-2.5-pro')
    response = text_model.generate_content(prompt)

    parsed_data = parse_llm_response_and_save(response.text)
    
    return {
        "message": "Onboarding data processed successfully",
        "meal_plan_count": len(parsed_data["meal_plan"]),
        "groceries_count": len(parsed_data["groceries"]),
        "files_saved": parsed_data["files_saved"]
    }
>>>>>>> Stashed changes
