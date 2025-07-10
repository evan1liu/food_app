<script lang="ts">
	import Groceries from './groceries.svelte';
	import MealPlan from './meal_plan.svelte';

	// These return promises, which we will handle in the template with #await
	const meal_plan_promise = fetch('http://127.0.0.1:8000/api/meal-plan').then(async (res) => {
		if (!res.ok) {
			const errorText = await res.text();
			throw new Error(`Failed to fetch meal plan: ${res.status} ${errorText}`);
		}
		// The AI returns a JSON array inside <meal> tags, so we need to extract it.
		const rawText = await res.text();
		const mealData = rawText.match(/<meal>([\s\S]*?)<\/meal>/);
		if (mealData && mealData[1]) {
			try {
				return JSON.parse(mealData[1]);
			} catch (e) {
				console.error('Failed to parse meal plan JSON:', e);
				throw new Error('Received malformed meal plan data from server.');
			}
		}
		throw new Error('Could not find meal plan data in the response.');
	});

	const groceries_promise = fetch('http://127.0.0.1:8000/api/groceries').then(async (res) => {
		if (!res.ok) {
			const errorText = await res.text();
			throw new Error(`Failed to fetch groceries: ${res.status} ${errorText}`);
		}
		// The AI may also wrap groceries in XML, so we handle that just in case.
		const rawText = await res.text();
		const groceryData = rawText.match(/<groceries>([\s\S]*?)<\/groceries>/);
		if (groceryData && groceryData[1]) {
			try {
				return JSON.parse(groceryData[1]);
			} catch (e) {
				console.error('Failed to parse groceries JSON:', e);
				throw new Error('Received malformed groceries data from server.');
			}
		}
		// Fallback to parsing the whole response as JSON if no tags are found.
		try {
			return JSON.parse(rawText);
		} catch (e) {
			console.error('Failed to parse groceries JSON:', e);
			throw new Error('Received malformed groceries data from server.');
		}
	});
</script>

<svelte:head>
	<title>Your Meal Plan</title>
	<meta name="description" content="Your weekly meal plan and grocery list." />
</svelte:head>

<div class="container">
	<h1>Your Meal Plan & Groceries</h1>

	{#await meal_plan_promise}
		<p>Loading meal plan...</p>
	{:then meal_plan}
		<MealPlan {meal_plan} />
	{:catch error}
		<p style="color: red">Error loading meal plan: {error.message}</p>
		<p>Please make sure the backend server is running and the API is available.</p>
	{/await}

	{#await groceries_promise}
		<p>Loading groceries...</p>
	{:then groceries}
		<Groceries {groceries} />
	{:catch error}
		<p style="color: red">Error loading groceries: {error.message}</p>
		<p>Please make sure the backend server is running and the API is available.</p>
	{/await}
</div>

<style>
	.container {
		max-width: 1200px;
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
</style>
