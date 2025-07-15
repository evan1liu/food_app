import sys
import os

# Add the virtual environment's site-packages to the system path
venv_path = os.path.join(os.path.dirname(__file__), '..', '.venv', 'Lib', 'site-packages')
if os.path.exists(venv_path):
    sys.path.insert(0, venv_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel
from routers import api_router
from home_routes import home_router
from onboarding_routes import onboarding_router

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allows your Svelte frontend to connect
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Create images directory if it doesn't exist
images_dir = os.path.join("backend", "images")
os.makedirs(images_dir, exist_ok=True)

# Serve static images
app.mount("/images", StaticFiles(directory=images_dir), name="images")

# Include the API router
app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Food App API"}


# Include the routers
app.include_router(onboarding_router, prefix="/api/onboarding", tags=["onboarding"])
app.include_router(home_router, prefix="/api", tags=["home"])


class OnboardingRequest(BaseModel):
    time_to_cook_per_day: float
    money_to_spend_per_week: float
    allergies: list[str]
    nutrition_goals: list[str]
    food_restrictions: list[str]
    food_preferences: dict[str, str]
    address: str # there could be a type for address
    

# @onboarding_router.post("/onboarding")
# async def onboarding_user():
    
#     await user_collection.update_one(
#         {"email": current_user.email},
#         {"$set": {
#             "major": user_data.major, 
#             "entry_year": user_data.entry_year,
#             "full_name": user_data.full_name,
#             "onboarded": True,
#             # Store hierarchical info for future use
#             "program_info": selected_program_info
#         }}
#     )

#     # Initialize a roadmap during onboarding with hierarchical info
#     await initialize_full_roadmap(
#         current_user.id, 
#         user_data.major, 
#         user_data.entry_year,
#         selected_program_info
#     )
#     return {"message": "User updated successfully"}
