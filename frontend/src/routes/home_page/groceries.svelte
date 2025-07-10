<script lang="ts">
	export let groceries: string[]; // Expecting an array of grocery item strings
</script>

<div class="groceries-container">
	<h2>Grocery List</h2>
	{#if groceries && groceries.length > 0}
		<ul class="grocery-list">
			{#each groceries as item}
				<li>{item}</li>
			{/each}
		</ul>
	{:else}
		<p>No groceries to show. Your grocery list will appear here once a meal plan is generated.</p>
	{/if}
</div>

<style>
	.groceries-container {
		margin-bottom: 2rem;
	}
	h2 {
		color: #333;
		border-bottom: 2px solid #eee;
		padding-bottom: 0.5rem;
		margin-bottom: 1.5rem;
	}
	.grocery-list {
		list-style: none;
		padding: 0;
		column-count: 3;
		column-gap: 2rem;
	}
	.grocery-list li {
		background: #f9f9f9;
		padding: 0.75rem 1rem;
		border-radius: 6px;
		margin-bottom: 0.5rem;
		break-inside: avoid;
	}
</style>
