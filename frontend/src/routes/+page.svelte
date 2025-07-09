<script lang="ts">
    import Step1 from "./Step1.svelte";
    import Step2 from "./Step2.svelte";
    const meal_categories = ["Mexican", "Indian", "Chinese"]
    let name = $state()
    // Create a state object with multiple properties
    let userProfile = $state({
        firstName: '',
        lastName: '',
        email: '',
        favoriteFood: '',
        age: ''
    })

    $inspect(userProfile)

    // Derived value to show the full name
    let fullName = $derived(userProfile.firstName + ' ' + userProfile.lastName)

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

    let step = $state()
</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>

<input type="text" bind:value={name} placeholder="Enter your name" />
{#if name}
    <p>{greetingMessage}</p>
{/if}

<a href="/meals"><h1>Go to Meal Page</h1></a>

{#each meal_categories as meal_category}
    <button onclick={() => logCategoryInConsole(meal_category)}>{meal_category} Food</button>
{/each}

<div>
    <label>
        First Name:
        <input type="text" bind:value={step} placeholder="Enter step" />
    </label>
</div>

{#if step === "1"}
    <Step1 {name}/>
{:else if step === "2"}
   <Step2 />
{/if}

<h2>User Profile Form</h2>

<!-- Each input binds to a specific property of the state object -->
<div>
    <label>
        First Name:
        <input type="text" bind:value={userProfile.firstName} placeholder="Enter first name" />
    </label>
</div>

<div>
    <label>
        Last Name:
        <input type="text" bind:value={userProfile.lastName} placeholder="Enter last name" />
    </label>
</div>

<div>
    <label>
        Email:
        <input type="email" bind:value={userProfile.email} placeholder="Enter email" />
    </label>
</div>

<div>
    <label>
        Favorite Food:
        <input type="text" bind:value={userProfile.favoriteFood} placeholder="Enter favorite food" />
    </label>
</div>

<div>
    <label>
        Age:
        <input type="number" bind:value={userProfile.age} placeholder="Enter age" />
    </label>
</div>

<!-- Display the current state to see reactive updates -->
{#if userProfile.firstName || userProfile.lastName}
    <h3>Hello, {fullName}!</h3>
{/if}

{#if userProfile.email}
    <p>Email: {userProfile.email}</p>
{/if}

{#if userProfile.favoriteFood}
    <p>Favorite Food: {userProfile.favoriteFood}</p>
{/if}

{#if userProfile.age}
    <p>Age: {userProfile.age}</p>
{/if}

<!-- Debug: Show the entire object -->
<details>
    <summary>Current State (Debug)</summary>
    <pre>{JSON.stringify(userProfile, null, 2)}</pre>
</details>


<style>

</style>