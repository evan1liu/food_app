<script>
    /** @type {string[]} */
    export let selectedAllergies = [];

    // Load allergies from backend
    async function loadAllergies() {
        const response = await fetch('http://127.0.0.1:8000/api/onboarding/get_allergies');
        if (response.ok) {
            return await response.json();
        } else {
            throw new Error('Could not load allergies. Please ensure the backend server is running.');
        }
    }

    let allergiesPromise = loadAllergies();

    /**
     * @param {string[]} currentAllergies
     */
    function gotoNextStep(currentAllergies) {
      console.log('Selected allergies:', currentAllergies);
      // TODO: Navigate to next step or submit data
    }
</script>

<h2>Select your allergies:</h2>

{#await allergiesPromise}
    <p>Loading allergies...</p>
{:then allergies}
    {#each allergies as allergy}
        <label>
            <input type="checkbox" bind:group={selectedAllergies} value={allergy} />
            {allergy}
        </label>
    {/each}
    <br/>
    <button on:click={() => gotoNextStep(selectedAllergies)}>Next</button>
{:catch error}
    <p style="color: red;">{error.message}</p>
{/await}
  