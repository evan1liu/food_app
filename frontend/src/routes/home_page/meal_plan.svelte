<script lang="ts">
	export let meal_plan: any[]; // Expecting an array of meal objects
	
	let selectedMeal: any = null;
	
	function selectMeal(meal: any) {
		selectedMeal = meal;
	}
	
	function closeMealDetails() {
		selectedMeal = null;
	}
</script>

<div class="meal-plan-container">
	<h2>Weekly Meal Plan</h2>
	{#if meal_plan && meal_plan.length > 0}
		<div class="meal-grid">
			{#each meal_plan as meal}
				<div class="meal-card">
					{#if meal.image_url}
						<img src={meal.image_url} alt={`AI-generated view of ${meal.meal_name}`} class="recipe-image" />
					{:else}
						<div class="image-placeholder">
							<span>No Image Available</span>
						</div>
					{/if}
					<div class="meal-content">
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
				</div>
			{/each}
		</div>
	{:else}
		<p>No meal plan available yet. Generate one to get started!</p>
	{/if}
</div>

<!-- Modal for detailed meal view -->
{#if selectedMeal}
	<div class="modal-overlay" on:click={closeMealDetails} on:keydown={(e) => e.key === 'Escape' && closeMealDetails()} role="button" tabindex="0">
		<div class="modal-content" on:click|stopPropagation>
			<button class="close-button" on:click={closeMealDetails}>✕</button>
			
			<div class="meal-header">
				<div class="meal-image-large">
					<div class="image-icon-large">🍽️</div>
				</div>
				<div class="meal-title-section">
					<h2>{selectedMeal.meal_name}</h2>
					<p><strong>Date:</strong> {selectedMeal.date_at_which_meal_should_be_cooked}</p>
					<p><strong>Prep Time:</strong> {selectedMeal.time_to_prepare} minutes</p>
				</div>
			</div>

			<div class="meal-details">
				<div class="details-column">
					<h4>Ingredients</h4>
					<ul>
						{#each selectedMeal.ingredients as ingredient}
							<li>{ingredient}</li>
						{/each}
					</ul>
				</div>

				<div class="details-column">
					<h4>Steps</h4>
					<ol>
						{#each selectedMeal.steps_to_prepare as step}
							<li>{step}</li>
						{/each}
					</ol>
				</div>
			</div>

			{#if selectedMeal.tips_and_tricks}
				<div class="tips-section">
					<h4>Tips & Tricks</h4>
					<p>{selectedMeal.tips_and_tricks}</p>
				</div>
			{/if}

			{#if selectedMeal.appliances_and_utensils && selectedMeal.appliances_and_utensils.length > 0}
				<div class="appliances-section">
					<h4>Appliances & Utensils</h4>
					<ul class="appliances-list">
						{#each selectedMeal.appliances_and_utensils as item}
							<li>{item}</li>
						{/each}
					</ul>
				</div>
			{/if}
		</div>
	</div>
{/if}

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
		background: #fff;
		border: 1px solid #ddd;
		border-radius: 12px;
		overflow: hidden; /* Ensures image corners are rounded */
		display: flex;
		flex-direction: column;
	}
	.recipe-image {
		width: 100%;
		height: 250px;
		object-fit: cover;
	}
	.image-placeholder {
		width: 100%;
		height: 250px;
		background-color: #f0f0f0;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #aaa;
	}
	.meal-content {
		padding: 1.5rem;
	}
	h3 {
		margin-top: 0;
		color: #444;
	}
	
	.meal-meta {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 0.5rem;
		font-size: 0.85rem;
		color: #666;
	}
	
	.meal-date {
		background: #e3f2fd;
		padding: 0.2rem 0.5rem;
		border-radius: 4px;
		font-weight: 500;
	}
	
	.meal-time {
		background: #f3e5f5;
		padding: 0.2rem 0.5rem;
		border-radius: 4px;
		font-weight: 500;
	}
	
	.ingredients-preview {
		font-size: 0.85rem;
		color: #777;
		line-height: 1.4;
	}
	
	.more-ingredients {
		color: #007bff;
		font-weight: 500;
	}

	/* Modal styles */
	.modal-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.5);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1000;
		padding: 2rem;
	}
	
	.modal-content {
		background: white;
		border-radius: 12px;
		max-width: 800px;
		max-height: 90vh;
		width: 100%;
		overflow-y: auto;
		position: relative;
		padding: 2rem;
	}
	
	.close-button {
		position: absolute;
		top: 1rem;
		right: 1rem;
		background: none;
		border: none;
		font-size: 1.5rem;
		cursor: pointer;
		color: #666;
		z-index: 1001;
	}
	
	.close-button:hover {
		color: #333;
	}
	
	.meal-header {
		display: flex;
		gap: 1.5rem;
		margin-bottom: 2rem;
	}
	
	.meal-image-large {
		width: 150px;
		height: 150px;
		background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
		border-radius: 12px;
		display: flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
	}
	
	.image-icon-large {
		font-size: 4rem;
		opacity: 0.7;
	}
	
	.meal-title-section h2 {
		margin: 0 0 1rem 0;
		color: #333;
	}
	
	.meal-details {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 2rem;
		margin-bottom: 2rem;
	}
	
	.details-column h4 {
		margin: 0 0 1rem 0;
		color: #555;
		border-bottom: 1px solid #eee;
		padding-bottom: 0.5rem;
	}
	
	.details-column ul,
	.details-column ol {
		padding-left: 1.2rem;
		margin: 0;
	}
	
	.details-column li {
		margin-bottom: 0.5rem;
		line-height: 1.4;
	}
	
	.tips-section,
	.appliances-section {
		margin-bottom: 1.5rem;
	}
	
	.tips-section h4,
	.appliances-section h4 {
		margin: 0 0 1rem 0;
		color: #555;
		border-bottom: 1px solid #eee;
		padding-bottom: 0.5rem;
	}
	
	.appliances-list {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
		list-style: none;
		padding: 0;
		margin: 0;
	}
	
	.appliances-list li {
		background: #f8f9fa;
		padding: 0.3rem 0.6rem;
		border-radius: 6px;
		font-size: 0.9rem;
		border: 1px solid #e9ecef;
	}

	@media (max-width: 768px) {
		.meal-grid {
			grid-template-columns: 1fr;
		}
		
		.meal-details {
			grid-template-columns: 1fr;
		}
		
		.meal-header {
			flex-direction: column;
		}
		
		.modal-overlay {
			padding: 1rem;
		}
		
		.modal-content {
			padding: 1.5rem;
		}
	}
</style>
