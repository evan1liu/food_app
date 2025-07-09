<script>
    let {timeToCookPerDay = $bindable()} = $props();
    let timeRanges = [
        { min: 0, max: 15, label: "0-15 minutes", icon: "⚡", description: "Quick & easy meals" },
        { min: 16, max: 30, label: "16-30 minutes", icon: "🥗", description: "Simple cooking" },
        { min: 31, max: 45, label: "31-45 minutes", icon: "🍳", description: "Moderate prep" },
        { min: 46, max: 60, label: "46-60 minutes", icon: "👨‍🍳", description: "Proper cooking" },
        { min: 61, max: 999, label: "60+ minutes", icon: "🔥", description: "Gourmet meals" }
    ];
    
    let selectedRange = $state(null);
    let customTime = $state('');
    let useCustom = $state(false);

    // Initialize selected range based on current time
    $effect(() => {
        if (timeToCookPerDay && !useCustom) {
            selectedRange = timeRanges.find(range => 
                timeToCookPerDay >= range.min && timeToCookPerDay <= range.max
            );
        }
    });

    function selectRange(range) {
        selectedRange = range;
        useCustom = false;
        customTime = '';
        // Set to middle of range for initial value
        timeToCookPerDay = range.max === 999 ? 90 : Math.round((range.min + range.max) / 2);
    }

    function toggleCustom() {
        useCustom = !useCustom;
        if (useCustom) {
            selectedRange = null;
            customTime = timeToCookPerDay || '';
        } else {
            customTime = '';
        }
    }

    function updateCustomTime() {
        const time = parseFloat(customTime);
        if (!isNaN(time) && time >= 0) {
            timeToCookPerDay = time;
        }
    }
</script>

<div class="time-container">
    <div class="header">
        <h2>How much time do you have to cook each day?</h2>
        <p class="subtitle">We'll suggest recipes that fit your schedule and cooking style</p>
    </div>

    <div class="time-options">
        <div class="range-grid">
            {#each timeRanges as range}
                <button
                    class="range-card {selectedRange === range ? 'selected' : ''}"
                    onclick={() => selectRange(range)}
                >
                    <div class="range-icon">{range.icon}</div>
                    <div class="range-label">{range.label}</div>
                    <div class="range-description">{range.description}</div>
                </button>
            {/each}
        </div>

        <div class="custom-option">
            <button
                class="custom-toggle {useCustom ? 'active' : ''}"
                onclick={toggleCustom}
            >
                {useCustom ? '✓' : '⏱️'} Custom Time
            </button>
            
            {#if useCustom}
                <div class="custom-input-container">
                    <div class="input-wrapper">
                        <input
                            type="number"
                            bind:value={customTime}
                            oninput={updateCustomTime}
                            placeholder="Enter minutes"
                            class="custom-input"
                            min="0"
                            step="1"
                        />
                        <span class="input-suffix">minutes per day</span>
                    </div>
                </div>
            {/if}
        </div>
    </div>

    {#if timeToCookPerDay}
        <div class="time-summary">
            <div class="summary-content">
                <h3>Your Cooking Time</h3>
                <div class="time-display">
                    <span class="amount">{timeToCookPerDay}</span>
                    <span class="period">minutes per day</span>
                </div>
                <div class="time-breakdown">
                    <div class="breakdown-item">
                        <span class="breakdown-label">Weekly</span>
                        <span class="breakdown-value">{Math.round(timeToCookPerDay * 7)} min</span>
                    </div>
                    <div class="breakdown-item">
                        <span class="breakdown-label">Per meal</span>
                        <span class="breakdown-value">~{Math.round(timeToCookPerDay / 3)} min</span>
                    </div>
                </div>
                <div class="cooking-tips">
                    {#if timeToCookPerDay <= 15}
                        <p>💡 Perfect for one-pot meals, pre-prepared ingredients, and quick assembly dishes</p>
                    {:else if timeToCookPerDay <= 30}
                        <p>💡 Great for stir-fries, simple pasta dishes, and fresh salads</p>
                    {:else if timeToCookPerDay <= 45}
                        <p>💡 Ideal for roasted vegetables, marinated proteins, and homemade soups</p>
                    {:else if timeToCookPerDay <= 60}
                        <p>💡 Perfect for slow-cooked meals, homemade bread, and elaborate dishes</p>
                    {:else}
                        <p>💡 Excellent for gourmet cooking, fermentation, and complex multi-course meals</p>
                    {/if}
                </div>
            </div>
        </div>
    {/if}
</div>

<style>
    .time-container {
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

    .time-options {
        margin-bottom: 2rem;
    }

    .range-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
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
        gap: 0.5rem;
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
        margin-bottom: 0.5rem;
    }

    .range-description {
        font-size: 0.9rem;
        color: #6c757d;
        font-style: italic;
    }

    .range-card.selected .range-description {
        color: #155724;
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
        max-width: 400px;
    }

    .custom-input {
        padding: 1rem;
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

    .time-summary {
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

    .time-display {
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

    .time-breakdown {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-bottom: 1.5rem;
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

    .cooking-tips {
        background: rgba(0, 123, 255, 0.1);
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1rem;
    }

    .cooking-tips p {
        margin: 0;
        color: #0056b3;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    @media (max-width: 768px) {
        .range-grid {
            grid-template-columns: 1fr;
        }
        
        .range-card {
            padding: 1.5rem 1rem;
        }
        
        .header h2 {
            font-size: 1.8rem;
        }
        
        .time-breakdown {
            gap: 1rem;
        }
    }
</style>