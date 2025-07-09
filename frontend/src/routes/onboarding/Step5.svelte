<script>
    /** @type {string[]} */
    export let selectedAllergies = [];
    /** @type {string[]} */
    let allergies = [];

    // Load allergies from backend
    async function loadAllergies() {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/onboarding/get_allergies');
            if (response.ok) {
                allergies = await response.json();
            } else {
                console.error('Failed to load allergies');
            }
        } catch (error) {
            console.error('Error loading allergies:', error);
        }
    }

    // Load allergies when component mounts
    loadAllergies();
  
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

    /**
     * @param {string[]} allergies
     */
    function gotoNextStep(allergies) {
      console.log('Selected allergies:', allergies);
      // TODO: Navigate to next step or submit data
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
  