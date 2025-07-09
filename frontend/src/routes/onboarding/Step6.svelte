<script>
    let {foodPreferences = $bindable()} = $props();

    // Available food preferences from backend
    let availableFoodPreferences = $state({});
    
    // Track which categories are expanded
    let expandedCategories = $state(new Set());
    
    // Loading state
    let loading = $state(true);
    let error = $state('');

    // Initialize foodPreferences if not already set
    if (!foodPreferences || typeof foodPreferences !== 'object') {
        foodPreferences = {};
    }

    // Load food preferences from backend
    async function loadFoodPreferences() {
        try {
            loading = true;
            error = '';
            const response = await fetch('http://127.0.0.1:8000/api/onboarding/get_food_preferences');
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            availableFoodPreferences = await response.json();
            
            // Initialize empty arrays for each category if not already present
            for (const category of Object.keys(availableFoodPreferences)) {
                if (!foodPreferences[category]) {
                    foodPreferences[category] = [];
                }
            }
        } catch (err) {
            console.error('Error loading food preferences:', err);
            error = 'Failed to load food preferences. Please try again.';
        } finally {
            loading = false;
        }
    }

    // Toggle category expansion
    function toggleCategory(category) {
        if (expandedCategories.has(category)) {
            expandedCategories.delete(category);
        } else {
            expandedCategories.add(category);
        }
        expandedCategories = new Set(expandedCategories); // Trigger reactivity
    }

    // Check if category is expanded
    function isCategoryExpanded(category) {
        return expandedCategories.has(category);
    }

    // Toggle selection of a food item in a specific category
    function toggleFoodItem(category, foodItem) {
        if (!foodPreferences[category]) {
            foodPreferences[category] = [];
        }
        
        const currentSelections = foodPreferences[category];
        if (currentSelections.includes(foodItem)) {
            // Remove if already selected
            foodPreferences[category] = currentSelections.filter(item => item !== foodItem);
        } else {
            // Add if not selected
            foodPreferences[category] = [...currentSelections, foodItem];
        }
    }

    // Check if a food item is selected
    function isFoodItemSelected(category, foodItem) {
        return foodPreferences[category]?.includes(foodItem) || false;
    }

    // Get selection count for a category
    function getCategorySelectionCount(category) {
        return foodPreferences[category]?.length || 0;
    }

    // Load food preferences when component mounts
    loadFoodPreferences();
</script>

<div class="food-preferences-container">
    <h2>Select Your Food Preferences</h2>
    <p>Click on categories to explore and select foods you enjoy:</p>

    {#if loading}
        <div class="loading">Loading food preferences...</div>
    {:else if error}
        <div class="error">
            {error}
            <button onclick={loadFoodPreferences} class="retry-button">Retry</button>
        </div>
    {:else}
        <div class="categories-container">
            {#each Object.entries(availableFoodPreferences) as [category, foods]}
                <div class="category-wrapper">
                    <!-- Category Tag -->
                    <button 
                        class="category-tag {isCategoryExpanded(category) ? 'expanded' : ''}"
                        onclick={() => toggleCategory(category)}
                    >
                        <span class="category-name">{category}</span>
                        <span class="selection-count">
                            {#if getCategorySelectionCount(category) > 0}
                                ({getCategorySelectionCount(category)})
                            {/if}
                        </span>
                        <span class="expand-icon">
                            {isCategoryExpanded(category) ? '▼' : '▶'}
                        </span>
                    </button>

                    <!-- Expanded Food Items -->
                    {#if isCategoryExpanded(category)}
                        <div class="food-items-container">
                            {#each foods as foodItem}
                                <button 
                                    class="food-item-tag {isFoodItemSelected(category, foodItem) ? 'selected' : ''}"
                                    onclick={() => toggleFoodItem(category, foodItem)}
                                >
                                    {foodItem}
                                </button>
                            {/each}
                        </div>
                    {/if}
                </div>
            {/each}
        </div>

        <!-- Summary of selections -->
        {#if Object.values(foodPreferences).some(selections => selections.length > 0)}
            <div class="summary">
                <h3>Your Selections:</h3>
                <div class="summary-tags">
                    {#each Object.entries(foodPreferences) as [category, selections]}
                        {#if selections.length > 0}
                            <div class="summary-category">
                                <span class="summary-category-name">{category}:</span>
                                {#each selections as selection}
                                    <span class="summary-item-tag">{selection}</span>
                                {/each}
                            </div>
                        {/if}
                    {/each}
                </div>
            </div>
        {/if}
    {/if}
</div>

<style>
    .food-preferences-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 2rem;
    }

    .loading, .error {
        text-align: center;
        padding: 2rem;
        font-size: 1.2rem;
    }

    .error {
        color: #dc3545;
    }

    .retry-button {
        margin-left: 1rem;
        padding: 0.5rem 1rem;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }

    .retry-button:hover {
        background-color: #0056b3;
    }

    .categories-container {
        margin: 2rem 0;
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        align-items: flex-start;
    }

    .category-wrapper {
        display: flex;
        flex-direction: column;
        min-width: 200px;
        max-width: 300px;
        flex: 1;
    }

    .category-tag {
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        padding: 0.75rem 1rem;
        background: linear-gradient(135deg, #007bff, #0056b3);
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 0.95rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 123, 255, 0.2);
    }

    .category-tag:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3);
    }

    .category-tag.expanded {
        background: linear-gradient(135deg, #28a745, #20c997);
        border-radius: 8px 8px 0 0;
    }

    .category-name {
        flex: 1;
        text-align: left;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .selection-count {
        color: #e3f2fd;
        font-weight: normal;
        margin-right: 0.5rem;
        font-size: 0.85rem;
    }

    .expand-icon {
        font-size: 0.8rem;
        transition: transform 0.3s ease;
        margin-left: 0.25rem;
    }

    .food-items-container {
        background: #f8f9fa;
        border: 2px solid #28a745;
        border-top: none;
        border-radius: 0 0 8px 8px;
        padding: 1rem;
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        width: 100%;
        box-sizing: border-box;
    }

    .food-item-tag {
        padding: 0.4rem 0.8rem;
        background: white;
        border: 2px solid #dee2e6;
        border-radius: 20px;
        cursor: pointer;
        font-size: 0.85rem;
        transition: all 0.2s ease;
        color: #495057;
        white-space: nowrap;
    }

    .food-item-tag:hover {
        border-color: #007bff;
        background: #e3f2fd;
        transform: scale(1.05);
    }

    .food-item-tag.selected {
        background: #007bff;
        color: white;
        border-color: #0056b3;
        box-shadow: 0 2px 4px rgba(0, 123, 255, 0.3);
    }

    .summary {
        margin-top: 3rem;
        padding: 2rem;
        background: linear-gradient(135deg, #e8f5e8, #f0f8f0);
        border-radius: 12px;
        border: 2px solid #28a745;
    }

    .summary h3 {
        margin: 0 0 1.5rem 0;
        color: #28a745;
        font-size: 1.3rem;
    }

    .summary-tags {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .summary-category {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 0.5rem;
    }

    .summary-category-name {
        font-weight: 600;
        color: #495057;
        margin-right: 0.5rem;
    }

    .summary-item-tag {
        padding: 0.3rem 0.6rem;
        background: #28a745;
        color: white;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 500;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .categories-container {
            gap: 0.75rem;
        }
        
        .category-wrapper {
            min-width: 150px;
            max-width: 250px;
        }
        
        .category-tag {
            font-size: 0.9rem;
            padding: 0.6rem 0.8rem;
        }
    }
</style>