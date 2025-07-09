<script>
    let {weeklyGroceryBudget = $bindable()} = $props();
    let budgetRanges = [
        { min: 0, max: 50, label: "$0 - $50", icon: "💰" },
        { min: 51, max: 100, label: "$51 - $100", icon: "💵" },
        { min: 101, max: 150, label: "$101 - $150", icon: "💸" },
        { min: 151, max: 200, label: "$151 - $200", icon: "💳" },
        { min: 201, max: 999, label: "$201+", icon: "🏦" }
    ];
    
    let selectedRange = $state(null);
    let customAmount = $state('');
    let useCustom = $state(false);

    // Initialize selected range based on current budget
    $effect(() => {
        if (weeklyGroceryBudget && !useCustom) {
            selectedRange = budgetRanges.find(range => 
                weeklyGroceryBudget >= range.min && weeklyGroceryBudget <= range.max
            );
        }
    });

    function selectRange(range) {
        selectedRange = range;
        useCustom = false;
        customAmount = '';
        // Set to middle of range for initial value
        weeklyGroceryBudget = range.max === 999 ? 250 : Math.round((range.min + range.max) / 2);
    }

    function toggleCustom() {
        useCustom = !useCustom;
        if (useCustom) {
            selectedRange = null;
            customAmount = weeklyGroceryBudget || '';
        } else {
            customAmount = '';
        }
    }

    function updateCustomAmount() {
        const amount = parseFloat(customAmount);
        if (!isNaN(amount) && amount >= 0) {
            weeklyGroceryBudget = amount;
        }
    }
</script>

<div class="budget-container">
    <div class="header">
        <h2>What's your weekly grocery budget?</h2>
        <p class="subtitle">This helps us recommend meals that fit your budget and suggest cost-effective ingredients</p>
    </div>

    <div class="budget-options">
        <div class="range-grid">
            {#each budgetRanges as range}
                <button
                    class="range-card {selectedRange === range ? 'selected' : ''}"
                    onclick={() => selectRange(range)}
                >
                    <div class="range-icon">{range.icon}</div>
                    <div class="range-label">{range.label}</div>
                </button>
            {/each}
        </div>

        <div class="custom-option">
            <button
                class="custom-toggle {useCustom ? 'active' : ''}"
                onclick={toggleCustom}
            >
                {useCustom ? '✓' : '📝'} Custom Amount
            </button>
            
            {#if useCustom}
                <div class="custom-input-container">
                    <div class="input-wrapper">
                        <span class="currency-symbol">$</span>
                        <input
                            type="number"
                            bind:value={customAmount}
                            oninput={updateCustomAmount}
                            placeholder="Enter amount"
                            class="custom-input"
                            min="0"
                            step="0.01"
                        />
                        <span class="input-suffix">per week</span>
                    </div>
                </div>
            {/if}
        </div>
    </div>

    {#if weeklyGroceryBudget}
        <div class="budget-summary">
            <div class="summary-content">
                <h3>Your Budget</h3>
                <div class="budget-display">
                    <span class="amount">${weeklyGroceryBudget}</span>
                    <span class="period">per week</span>
                </div>
                <div class="budget-breakdown">
                    <div class="breakdown-item">
                        <span class="breakdown-label">Monthly</span>
                        <span class="breakdown-value">~${Math.round(weeklyGroceryBudget * 4.33)}</span>
                    </div>
                    <div class="breakdown-item">
                        <span class="breakdown-label">Daily</span>
                        <span class="breakdown-value">~${Math.round(weeklyGroceryBudget / 7)}</span>
                    </div>
                </div>
            </div>
        </div>
    {/if}
</div>

<style>
    .budget-container {
        max-width: 700px;
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

    .budget-options {
        margin-bottom: 2rem;
    }

    .range-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }

    .range-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 2rem 1rem;
        background: white;
        border: 2px solid #e1e8ed;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: center;
        gap: 1rem;
    }

    .range-card:hover {
        border-color: #007bff;
        box-shadow: 0 4px 12px rgba(0, 123, 255, 0.15);
        transform: translateY(-2px);
    }

    .range-card.selected {
        border-color: #28a745;
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        color: #155724;
    }

    .range-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    .range-label {
        font-size: 1.1rem;
        font-weight: 600;
    }

    .custom-option {
        text-align: center;
        margin-top: 2rem;
    }

    .custom-toggle {
        background: #f8f9fa;
        border: 2px solid #dee2e6;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        cursor: pointer;
        font-size: 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }

    .custom-toggle:hover {
        border-color: #007bff;
        background: #e3f2fd;
    }

    .custom-toggle.active {
        background: #007bff;
        border-color: #007bff;
        color: white;
    }

    .custom-input-container {
        margin-top: 1rem;
        display: flex;
        justify-content: center;
    }

    .input-wrapper {
        position: relative;
        display: inline-flex;
        align-items: center;
        max-width: 300px;
    }

    .currency-symbol {
        position: absolute;
        left: 1rem;
        color: #6c757d;
        font-size: 1.1rem;
        font-weight: 500;
        z-index: 1;
    }

    .custom-input {
        padding: 1rem 1rem 1rem 2.5rem;
        border: 2px solid #e1e8ed;
        border-radius: 8px;
        font-size: 1.1rem;
        font-weight: 500;
        text-align: center;
        width: 150px;
        transition: border-color 0.2s ease;
    }

    .custom-input:focus {
        outline: none;
        border-color: #007bff;
        box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
    }

    .input-suffix {
        margin-left: 1rem;
        color: #6c757d;
        font-size: 0.9rem;
        font-weight: 500;
    }

    .budget-summary {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        border: 2px solid #007bff;
        box-shadow: 0 4px 12px rgba(0, 123, 255, 0.1);
    }

    .summary-content h3 {
        color: #007bff;
        margin-bottom: 1rem;
        font-size: 1.3rem;
    }

    .budget-display {
        margin-bottom: 1.5rem;
    }

    .amount {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin-right: 0.5rem;
    }

    .period {
        font-size: 1.1rem;
        color: #6c757d;
        font-weight: 500;
    }

    .budget-breakdown {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 1rem;
    }

    .breakdown-item {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .breakdown-label {
        font-size: 0.9rem;
        color: #6c757d;
        margin-bottom: 0.25rem;
    }

    .breakdown-value {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2c3e50;
    }

    @media (max-width: 768px) {
        .range-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .range-card {
            padding: 1.5rem 1rem;
        }
        
        .header h2 {
            font-size: 1.8rem;
        }
        
        .budget-breakdown {
            gap: 1rem;
        }
    }
</style>