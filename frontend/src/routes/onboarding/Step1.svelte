<script>
    import availableRestrictions from '$lib/data/food_restrictions.json';

    let {selectedRestrictions = $bindable()} = $props();
    
    // Track which categories are expanded
    let expandedCategories = $state(new Set());

    // Initialize selectedRestrictions if not already set
    if (!selectedRestrictions || typeof selectedRestrictions !== 'object') {
        selectedRestrictions = {};
    }

    // Initialize empty arrays for each category if not already present
    for (const category of Object.keys(availableRestrictions)) {
        if (!selectedRestrictions[category]) {
            selectedRestrictions[category] = [];
        }
    }

    // Toggle category expansion
    /** @param {string} category */
    function toggleCategory(category) {
        if (expandedCategories.has(category)) {
            expandedCategories.delete(category);
        } else {
            expandedCategories.add(category);
        }
        expandedCategories = new Set(expandedCategories); // Trigger reactivity
    }

    // Check if category is expanded
    /** @param {string} category */
    function isCategoryExpanded(category) {
        return expandedCategories.has(category);
    }

    // Toggle selection of a food item in a specific category
    /** 
     * @param {string} category 
     * @param {string} restriction 
     */
    function toggleRestriction(category, restriction) {
        if (!selectedRestrictions[category]) {
            selectedRestrictions[category] = [];
        }
        
        const currentSelections = selectedRestrictions[category];
        if (currentSelections.includes(restriction)) {
            // Remove if already selected
            selectedRestrictions[category] = currentSelections.filter(/** @param {string} item */ item => item !== restriction);
        } else {
            // Add if not selected
            selectedRestrictions[category] = [...currentSelections, restriction];
        }
    }

    // Check if a food item is selected
    /** 
     * @param {string} category 
     * @param {string} restriction 
     */
    function isRestrictionSelected(category, restriction) {
        return selectedRestrictions[category]?.includes(restriction) || false;
    }

    // Get selection count for a category
    /** @param {string} category */
    function getCategorySelectionCount(category) {
        return selectedRestrictions[category]?.length || 0;
    }
</script>

<div class="food-restrictions-container">
    <h2>Select Your Food Restrictions</h2>
    <p>Click on categories to explore and select any applicable restrictions:</p>

    <div class="categories-container">
        {#each Object.entries(availableRestrictions) as [category, restrictions]}
            <div class="category-wrapper">
                <!-- Category Tag -->
                <button 
                    class="category-tag {isCategoryExpanded(category) ? 'expanded' : ''}"
                    onclick={() => toggleCategory(category)}
                >
                    <span class="category-name">{category.replace(/_/g, ' ')}</span>
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
                    <div class="restriction-items-container">
                        {#each restrictions as restriction}
                            <button 
                                class="restriction-item-tag {isRestrictionSelected(category, restriction) ? 'selected' : ''}"
                                onclick={() => toggleRestriction(category, restriction)}
                            >
                                {restriction}
                            </button>
                        {/each}
                    </div>
                {/if}
            </div>
        {/each}
    </div>

    <!-- Summary of selections -->
    {#if Object.values(selectedRestrictions).some(selections => selections.length > 0)}
        <div class="summary">
            <h3>Your Selections:</h3>
            <div class="summary-tags">
                {#each Object.entries(selectedRestrictions) as [category, selections]}
                    {#if selections.length > 0}
                        <div class="summary-category">
                            <span class="summary-category-name">{category.replace(/_/g, ' ')}:</span>
                            {#each selections as selection}
                                <span class="summary-item-tag">{selection}</span>
                            {/each}
                        </div>
                    {/if}
                {/each}
            </div>
        </div>
    {/if}
</div>

<style>
    .food-restrictions-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 2rem;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
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
        background: linear-gradient(135deg, #6c757d, #343a40);
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 0.95rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        text-transform: capitalize;
    }

    .category-tag:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }

    .category-tag.expanded {
        background: linear-gradient(135deg, #17a2b8, #117a8b);
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
        color: #e9ecef;
        font-weight: normal;
        margin-right: 0.5rem;
        font-size: 0.85rem;
    }

    .expand-icon {
        font-size: 0.8rem;
    }

    .restriction-items-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        padding: 1rem;
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-top: none;
        border-radius: 0 0 8px 8px;
    }

    .restriction-item-tag {
        padding: 0.5rem 1rem;
        background-color: #e9ecef;
        border: 1px solid #ced4da;
        border-radius: 20px;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .restriction-item-tag:hover {
        background-color: #dee2e6;
    }

    .restriction-item-tag.selected {
        background-color: #17a2b8;
        color: white;
        border-color: #117a8b;
    }

    .summary {
        margin-top: 2rem;
        padding: 1.5rem;
        background-color: #f8f9fa;
        border-radius: 8px;
    }

    .summary-tags {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .summary-category-name {
        font-weight: 600;
        margin-right: 0.5rem;
        text-transform: capitalize;
    }

    .summary-item-tag {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        background-color: #e9ecef;
        border-radius: 15px;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
</style>