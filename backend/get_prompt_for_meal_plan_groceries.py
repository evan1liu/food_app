from backend.models import OnboardingRequest

def get_prompt_for_meal_plan_groceries(onboarding_data):
    """
    Generates a detailed prompt for a meal plan generator AI
    based on the user's onboarding data.
    """

    # Start building the 'inputs' part of the prompt
    inputs = [
        f"- **Budget:** ${onboarding_data.money_to_spend_per_week} per week",
        f"- **Maximum cooking time per meal:** {onboarding_data.time_to_cook_per_day} minutes"
    ]

    # Start building the 'task' part of the prompt for the AI
    tasks = [
        f"- Only use groceries that can be purchased for less than ${onboarding_data.money_to_spend_per_week} for the week.",
        f"- Each meal must be preparable within {onboarding_data.time_to_cook_per_day} minutes."
    ]

    # Conditionally add user preferences if they are not empty
    if onboarding_data.allergies:
        allergies_str = ", ".join(onboarding_data.allergies)
        inputs.append(f"- **Allergies:** {allergies_str}")
        tasks.append(f"- No meal should contain ingredients from the allergies list: {allergies_str}.")

    active_food_restrictions = {k: v for k, v in onboarding_data.food_restrictions.items() if v}
    if active_food_restrictions:
        inputs.append(f"- **Food restrictions:** {active_food_restrictions}")
        tasks.append(f"- All meals must comply with the specified food restrictions: {active_food_restrictions}.")

    active_food_preferences = {k: v for k, v in onboarding_data.food_preferences.items() if v}
    if active_food_preferences:
        inputs.append(f"- **Food preferences:** {active_food_preferences}")
        tasks.append(f"- Prioritize recipes that align with user's food preferences: {active_food_preferences}.")

    if onboarding_data.nutrition_goals:
        goals_str = ", ".join(onboarding_data.nutrition_goals)
        inputs.append(f"- **Nutrition goals:** {goals_str}")
        tasks.append(f"- The overall meal plan must support the user's nutrition goals: {goals_str}.")

    # Join the parts to form the final prompt sections
    inputs_section = "\n    ".join(inputs)
    tasks_section = "\n    ".join(tasks)

    prompt = f"""
    You are an expert meal plan generator.

    Given the following user preferences:
    {inputs_section}

    **Your task is as follows:**

    **1. Generate a 7-day meal plan and a corresponding grocery list.**
    {tasks_section}

    **2. Format the output correctly into two distinct JSON arrays, each wrapped in XML tags.**

    **A. Meal Plan:**
    - The meal plan must be a single array of JSON objects.
    - Each object represents a meal and must have the following keys:
        - "meal_name": A descriptive name for the meal.
        - "image_prompt": A short, descriptive prompt for an image generation AI to create a photo of the final dish (e.g., "A vibrant bowl of spicy shrimp stir-fry with fresh vegetables on a dark plate").
        - "date_at_which_meal_should_be_cooked": The suggested date (e.g., "Day 1").
        - "ingredients": A list of all ingredients required.
        - "time_to_prepare": Estimated time in minutes.
        - "steps_to_prepare": A list of step-by-step instructions.
        - "tips_and_tricks": Optional tips or variations.
        - "appliances_and_utensils": A list of necessary kitchen tools.
    - **Wrap the entire JSON array in `<meal>` and `</meal>` tags.**

    **B. Grocery List:**
    - The grocery list must be a JSON array of objects.
    - Each object must have the following keys:
        - "item_name": The name of the grocery item.
        - "quantity": The amount needed (e.g., "2 lbs", "1 carton").
        - "estimated_cost": An estimated cost in USD (as a number, not a string).
    - The total estimated cost of all groceries must not exceed the user's budget of ${onboarding_data.money_to_spend_per_week}.
    - **Wrap the entire JSON array in `<groceries>` and `</groceries>` tags.**

    **CRITICAL: Your final output must only be the two XML blocks. Do not include any other text, explanations, or markdown formatting between or around them.**
    """
    return prompt.strip()