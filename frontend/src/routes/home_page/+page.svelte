<script lang="ts">
	import Groceries from './groceries.svelte';
	import MealPlan from './meal_plan.svelte';

	// These return promises, which we will handle in the template with #await
	const meal_plan_promise = fetch('http://127.0.0.1:8000/api/home/meal_plan').then(async (res) => {
		if (!res.ok) {
			const errorText = await res.text();
			throw new Error(`Failed to fetch meal plan: ${res.status} ${errorText}`);
		}
		// The backend returns JSON directly, no need to parse XML tags
		return await res.json();
	});

	const groceries_promise = fetch('http://127.0.0.1:8000/api/home/groceries').then(async (res) => {
		if (!res.ok) {
			const errorText = await res.text();
			throw new Error(`Failed to fetch groceries: ${res.status} ${errorText}`);
		}
		// The backend returns JSON directly, no need to parse XML tags
		return await res.json();
	});
</script>

<svelte:head>
	<title>Your Meal Plan</title>
	<meta name="description" content="Your weekly meal plan and grocery list." />
</svelte:head>

<div class="container">
	<h1>Your Meal Plan & Groceries</h1>
	
	<div class="main-layout">
		<div class="meal-plan-section">
			{#await meal_plan_promise}
				<p>Loading meal plan...</p>
			{:then meal_plan}
				<MealPlan {meal_plan} />
			{:catch error}
				<p style="color: red">Error loading meal plan: {error.message}</p>
				<p>Please make sure the backend server is running and the API is available.</p>
			{/await}
		</div>

		<div class="groceries-section">
			{#await groceries_promise}
				<p>Loading groceries...</p>
			{:then groceries}
				<Groceries {groceries} />
			{:catch error}
				<p style="color: red">Error loading groceries: {error.message}</p>
				<p>Please make sure the backend server is running and the API is available.</p>
			{/await}
		</div>
	</div>
</div>

<style>
	.container {
		max-width: 1400px;
		margin: 0 auto;
		padding: 2rem;
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell,
			'Open Sans', 'Helvetica Neue', sans-serif;
	}

	h1 {
		text-align: center;
		margin-bottom: 2rem;
		color: #333;
	}

	.main-layout {
		display: grid;
		grid-template-columns: 2fr 1fr;
		gap: 2rem;
		min-height: 70vh;
	}

	.meal-plan-section {
		overflow-y: auto;
	}

	.groceries-section {
		position: sticky;
		top: 2rem;
		height: fit-content;
		max-height: 80vh;
		overflow-y: auto;
	}

	@media (max-width: 768px) {
		.main-layout {
			grid-template-columns: 1fr;
		}
		
		.groceries-section {
			position: static;
		}
	}
</style>
