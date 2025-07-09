<script>
    let {weeklyGroceryBudget = $bindable()} = $props();
</script>

<h1>How much money can you spend per week on groceries</h1>

<input type="number" bind:value={weeklyGroceryBudget} placeholder="Enter your weekly grocery budget">