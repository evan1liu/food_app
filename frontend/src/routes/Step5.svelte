<script>
    /** @type {string[]} */
    export let selectedAllergies = [];
    const allergies = [
      "Peanuts", "Tree nuts", "Milk", "Eggs", "Fish", "Shellfish",
      "Wheat", "Soy", "Sesame", "Gluten", "Mustard", "Celery",
      "Sulfites", "Lupin", "Molluscs"
    ];
  
    /**
     * @param {string} allergy
     */
    function toggleAllergy(allergy) {
      if (selectedAllergies.includes(allergy)) {
        selectedAllergies = selectedAllergies.filter(a => a !== allergy);
      } else {
        selectedAllergies = [...selectedAllergies, allergy];
      }
    }
  </script>
  
  <h2>Select your allergies:</h2>
  {#each allergies as allergy}
    <label>
      <input type="checkbox" bind:group={selectedAllergies} value={allergy} />
      {allergy}
    </label>
  {/each}
  
  <button on:click={() => gotoNextStep(selectedAllergies)}>Next</button>
  