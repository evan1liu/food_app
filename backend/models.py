from pydantic import BaseModel

class OnboardingRequest(BaseModel):
    time_to_cook_per_day: float
    money_to_spend_per_week: float
    allergies: list[str]
    nutrition_goals: list[str]
    food_restrictions: dict[str, list[str]]
    food_preferences: dict[str, list[str]]
    address: str