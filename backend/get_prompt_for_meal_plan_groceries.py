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

    **1. Generate a 7-day meal plan.**
    {tasks_section}

    **2. Format the output correctly:**
    - The entire output must be a single array of JSON objects.
    - Each object in the array represents a meal and must have the following keys:
        - "meal_name": A descriptive name for the meal.
        - "date_at_which_meal_should_be_cooked": The suggested date for cooking the meal (e.g., "Day 1", "2024-07-10").
        - "ingredients": A list of all ingredients required.
        - "time_to_prepare": Estimated preparation and cooking time in minutes.
        - "steps_to_prepare": A list of step-by-step instructions.
        - "tips_and_tricks": Optional tips or variations for the recipe.
        - "appliances_and_utensils": A list of necessary kitchen tools.

    **3. Enclose the entire JSON array in `<meal>` and `</meal>` tags.**

    **Example of a single meal object:**
    {{
        "meal_name": "Quick Lemon Herb Chicken",
        "date_at_which_meal_should_be_cooked": "Day 1",
        "ingredients": ["1 lb chicken breast", "1 lemon", "1 tbsp olive oil", "herbs"],
        "time_to_prepare": 20,
        "steps_to_prepare": ["1. Preheat oven...", "2. Season chicken..."],
        "tips_and_tricks": "Goes well with a side of steamed vegetables.",
        "appliances_and_utensils": ["baking sheet", "oven", "knife"]
    }}

    4. **Generate a grocery list**:
    - The grocery list must be a JSON array of objects.
    - Each object in the array represents a grocery item and must have the following keys:
        - "item_name": The name of the grocery item as a string.
        - "quantity": The quantity of the grocery item as a string.
        - "estimated_cost": The estimated price of the grocery item as float.
    - Include all grocery items needed for the meal plan.
    - Only include groceries that can be purchased from supermarkets within {onboarding_data.money_to_spend_per_week} per week.
    - **Wrap the grocery list in XML tags**:  
      `<groceries>[ ...grocery list here... ]</groceries>`
    
    **CRITICAL: Your final output must only be the XML block containing the JSON array. Do not include any other text, explanations, or markdown formatting.**
    """
    return prompt.strip()