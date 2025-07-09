from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def read_root():
    return {"Hello": "World"}

class MealCategoryRequest(BaseModel):
    meal_category: str

@app.post("/meal_category")
async def print_meal_category(request: MealCategoryRequest):
    print(request.meal_category)
    
    return f"{request.meal_category} successfully printed"

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
