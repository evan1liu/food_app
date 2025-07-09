<script lang="ts">
    const meal_categories = ["Mexican", "Chinese", "Indian"]

    async function logCategoryInConsole(meal_category: string) {
        console.log(meal_category)

        const response = await fetch(`http://127.0.0.1:8000/meal_category`, {
				method: 'POST',
                headers: {
						'Content-Type': 'application/json'
					},
				body: JSON.stringify({ meal_category: meal_category })
			});
    }
</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>

<a href="/meals"><h1>Go to Meal Page</h1></a>

{#each meal_categories as meal_category}
    <button onclick={() => logCategoryInConsole(meal_category)}>{meal_category} Food</button>
{/each}

<style>

</style>