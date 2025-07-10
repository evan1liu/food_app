<script lang="ts">
	export let groceries: Array<{item_name: string, quantity: string, estimated_cost: number}>; // Expecting an array of grocery item objects
</script>

<div class="groceries-container">
	<h2>Grocery List</h2>
	{#if groceries && groceries.length > 0}
		<ul class="grocery-list">
			{#each groceries as item}
				<li>
					<span class="item-name">{item.item_name}</span>
					<span class="item-details">
						<span class="quantity">{item.quantity}</span>
						<span class="cost">${item.estimated_cost.toFixed(2)}</span>
					</span>
				</li>
			{/each}
		</ul>
		<div class="total-cost">
			<strong>Estimated Total: ${groceries.reduce((sum, item) => sum + item.estimated_cost, 0).toFixed(2)}</strong>
		</div>
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
		column-count: 2;
		column-gap: 2rem;
	}
	.grocery-list li {
		background: #f9f9f9;
		padding: 0.75rem 1rem;
		border-radius: 6px;
		margin-bottom: 0.5rem;
		break-inside: avoid;
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	.item-name {
		font-weight: 500;
		color: #333;
	}
	.item-details {
		display: flex;
		gap: 1rem;
		font-size: 0.9rem;
		color: #666;
	}
	.quantity {
		background: #e3f2fd;
		padding: 0.2rem 0.5rem;
		border-radius: 4px;
	}
	.cost {
		background: #e8f5e8;
		padding: 0.2rem 0.5rem;
		border-radius: 4px;
		font-weight: 500;
	}
	.total-cost {
		margin-top: 1rem;
		padding: 1rem;
		background: #f0f0f0;
		border-radius: 6px;
		text-align: right;
		font-size: 1.1rem;
	}
</style>
