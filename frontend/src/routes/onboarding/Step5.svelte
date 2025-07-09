<script>
    let {timeToCookPerDay = $bindable()} = $props();
</script>

<h1>How much time do you have to cook per day</h1>

<input type="number" bind:value={timeToCookPerDay} placeholder="Enter your time to cook per day">