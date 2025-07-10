<script lang="ts">
	export let meal_plan: any[]; // Expecting an array of meal objects
</script>

<div class="meal-plan-container">
	<h2>Weekly Meal Plan</h2>
	{#if meal_plan && meal_plan.length > 0}
		<div class="meal-grid">
			{#each meal_plan as meal}
				<div class="meal-card">
					<h3>{meal.meal_name}</h3>
					<p><strong>Date:</strong> {meal.date_at_which_meal_should_be_cooked}</p>
					<p><strong>Prep Time:</strong> {meal.time_to_prepare} minutes</p>

					<h4>Ingredients</h4>
					<ul>
						{#each meal.ingredients as ingredient}
							<li>{ingredient}</li>
						{/each}
					</ul>

					<h4>Steps</h4>
					<ol>
						{#each meal.steps_to_prepare as step}
							<li>{step}</li>
						{/each}
					</ol>

					{#if meal.tips_and_tricks}
						<h4>Tips & Tricks</h4>
						<p>{meal.tips_and_tricks}</p>
					{/if}

					{#if meal.appliances_and_utensils && meal.appliances_and_utensils.length > 0}
						<h4>Appliances & Utensils</h4>
						<ul>
							{#each meal.appliances_and_utensils as item}
								<li>{item}</li>
							{/each}
						</ul>
					{/if}
				</div>
			{/each}
		</div>
	{:else}
		<p>No meal plan available yet. Generate one to get started!</p>
	{/if}
</div>

<style>
	.meal-plan-container {
		margin-bottom: 2rem;
	}
	h2 {
		color: #333;
		border-bottom: 2px solid #eee;
		padding-bottom: 0.5rem;
		margin-bottom: 1.5rem;
	}
	.meal-grid {
		display: grid;
		grid-template-columns: 1fr;
		gap: 1.5rem;
	}
	.meal-card {
		background: #f9f9f9;
		border: 1px solid #ddd;
		border-radius: 8px;
		padding: 1.5rem;
	}
	h3 {
		margin-top: 0;
		color: #444;
	}
	h4 {
		margin-top: 1.5rem;
		margin-bottom: 0.5rem;
		color: #555;
	}
	ul,
	ol {
		padding-left: 1.2rem;
		margin-bottom: 0;
	}
</style>
