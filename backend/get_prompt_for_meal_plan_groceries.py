def get_prompt_for_meal_plan_groceries(onboarding_data):
    prompt = f"""
    You are an expert meal plan generator.

    Given the following inputs:
    - **Budget:** {onboarding_data.budget}
    - **Maximum cooking time per meal:** {onboarding_data.time_per_meal}
    - **Allergies:** {onboarding_data.allergies}
    - **Food restrictions:** {onboarding_data.food_restrictions}
    - **Food preferences:** {onboarding_data.food_preferences}
    - **Nutrition goals:** {onboarding_data.nutrition_goals}

    **Your task is as follows:**

    **Generate a week-long meal plan**:
    - Only use groceries that can be purchased for less than {onboarding_data.budget} dollars.
    - Each meal must be prepared within {onboarding_data.time_per_meal}.
    - No meal should contain ingredients from {onboarding_data.allergies}.
    - All meals must comply with the restrictions in {onboarding_data.food_restrictions}.
    - Prioritize recipes that align with {onboarding_data.food_preferences}.
    - Ensure the overall plan supports the user's {onboarding_data.nutrition_goals}.
    - Format the meal plan as an array of JSON objects, where each object has:
        - "meal_name"
        - "date_at_which_meal_should_be_cooked"
        - "ingredients"
        - "time_to_prepare"
        - "steps_to_prepare"
        - "tips&tricks"
        - "Appliances_and_utensils"

    - **Wrap the entire meal plan in XML tags**:  
      `<meal>[ ...meal plan here... ]</meal>`

    **Output only the XML blocks. Do not include any other text or commentary.**
    """
    return prompt