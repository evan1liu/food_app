<script>
    /** @type {string[]} */
    let { selectedAllergies = $bindable([]) } = $props();
    /** @type {string[]} */
    let allergies = $state([]);
    let loading = $state(true);
    let error = $state('');

    // Load allergies from backend
    async function loadAllergies() {
        try {
            loading = true;
            error = '';
            const response = await fetch('http://127.0.0.1:8000/api/onboarding/allergies');
            if (response.ok) {
                allergies = await response.json();
            } else {
                throw new Error('Failed to load allergies');
            }
        } catch (err) {
            console.error('Error loading allergies:', err);
            error = 'Failed to load allergies. Please try again.';
        } finally {
            loading = false;
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
     * @param {string} allergy
     */
    function isSelected(allergy) {
        return selectedAllergies.includes(allergy);
    }
</script>

<div class="allergies-container">
    <div class="header">
        <h2>Do you have any food allergies?</h2>
        <p class="subtitle">Select all that apply to ensure we recommend safe meals for you</p>
    </div>

    {#if loading}
        <div class="loading">
            <div class="loading-spinner"></div>
            <p>Loading allergies...</p>
        </div>
    {:else if error}
        <div class="error">
            <div class="error-icon">⚠️</div>
            <p>{error}</p>
            <button class="retry-btn" onclick={loadAllergies}>Try Again</button>
        </div>
    {:else}
        <div class="allergies-grid">
            {#each allergies as allergy}
                <button
                    class="allergy-card {isSelected(allergy) ? 'selected' : ''}"
                    onclick={() => toggleAllergy(allergy)}
                >
                    <div class="allergy-icon">
                        {#if isSelected(allergy)}
                            ✓
                        {:else}
                            🚫
                        {/if}
                    </div>
                    <span class="allergy-name">{allergy}</span>
                </button>
            {/each}
        </div>

        {#if selectedAllergies.length > 0}
            <div class="summary">
                <h3>Selected Allergies:</h3>
                <div class="selected-tags">
                    {#each selectedAllergies as allergy}
                        <span class="selected-tag">
                            {allergy}
                            <button class="remove-tag" onclick={() => toggleAllergy(allergy)}>×</button>
                        </span>
                    {/each}
                </div>
            </div>
        {/if}
    {/if}
</div>

<style>
    .allergies-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
    }

    .header {
        text-align: center;
        margin-bottom: 3rem;
    }

    .header h2 {
        font-size: 2.2rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 1rem;
    }

    .subtitle {
        font-size: 1.1rem;
        color: #6c757d;
        line-height: 1.6;
        max-width: 500px;
        margin: 0 auto;
    }

    .loading, .error {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem;
        text-align: center;
    }

    .loading-spinner {
        width: 40px;
        height: 40px;
        border: 3px solid #e1e8ed;
        border-top: 3px solid #007bff;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-bottom: 1rem;
    }

    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    .error {
        color: #dc3545;
    }

    .error-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }

    .retry-btn {
        margin-top: 1rem;
        padding: 0.75rem 1.5rem;
        background: #007bff;
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 500;
        transition: background 0.2s ease;
    }

    .retry-btn:hover {
        background: #0056b3;
    }

    .allergies-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }

    .allergy-card {
        display: flex;
        align-items: center;
        padding: 1.5rem;
        background: white;
        border: 2px solid #e1e8ed;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: left;
        font-size: 1rem;
        gap: 1rem;
    }

    .allergy-card:hover {
        border-color: #007bff;
        box-shadow: 0 4px 12px rgba(0, 123, 255, 0.15);
        transform: translateY(-2px);
    }

    .allergy-card.selected {
        border-color: #28a745;
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        color: #155724;
    }

    .allergy-icon {
        font-size: 1.5rem;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #f8f9fa;
        flex-shrink: 0;
    }

    .allergy-card.selected .allergy-icon {
        background: #28a745;
        color: white;
    }

    .allergy-name {
        font-weight: 500;
        flex: 1;
    }

    .summary {
        background: linear-gradient(135deg, #e8f5e8, #f0f8f0);
        padding: 2rem;
        border-radius: 12px;
        border: 2px solid #28a745;
        margin-top: 2rem;
    }

    .summary h3 {
        margin: 0 0 1rem 0;
        color: #28a745;
        font-size: 1.3rem;
    }

    .selected-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }

    .selected-tag {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: #28a745;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
    }

    .remove-tag {
        background: rgba(255, 255, 255, 0.3);
        border: none;
        color: white;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        cursor: pointer;
        font-size: 0.8rem;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: background 0.2s ease;
    }

    .remove-tag:hover {
        background: rgba(255, 255, 255, 0.5);
    }

    @media (max-width: 768px) {
        .allergies-grid {
            grid-template-columns: 1fr;
        }
        
        .allergy-card {
            padding: 1.2rem;
        }
        
        .header h2 {
            font-size: 1.8rem;
        }
    }
</style>
