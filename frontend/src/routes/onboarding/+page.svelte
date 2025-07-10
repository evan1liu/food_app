<script>
    import Step1 from "./Step1.svelte";
    import Step2 from "./Step2.svelte";
    import Step3 from "./Step3.svelte";
    import Step4 from "./Step4.svelte";
    import Step5 from "./Step5.svelte";
    import Step6 from "./Step6.svelte";
    import Step7 from "./Step7.svelte";

    let currentStep = $state(1);
    const totalSteps = 7;

    // Add loading and completion states
    let isSubmitting = $state(false);
    let isCompleted = $state(false);
    let submitError = $state(null);

    // Example function to submit onboarding data
    async function submitOnboarding(onboardingData) {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/submit_onboarding', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(onboardingData)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            console.log('Onboarding successful:', result);
            return result;
        } catch (error) {
            console.error('Error submitting onboarding:', error);
            throw error;
        }
    }

    let onboardingData = $state({
        food_restrictions: [],
        allergies: [],
        nutrition_goals: [],
        money_to_spend_per_week: 0,
        time_to_cook_per_day: 0,
        food_preferences: {},
        address: ''
    });

    function nextStep() {
        if (currentStep < totalSteps) {
            currentStep++;
        }
    }

    function previousStep() {
        if (currentStep > 1) {
            currentStep--;
        }
    }

    function goToStep(step) {
        if (step >= 1 && step <= totalSteps) {
            currentStep = step;
        }
    }

    // Handle completion/submission
    async function handleComplete() {
        if (currentStep === totalSteps) {
            // Submit the onboarding data
            try {
                isSubmitting = true;
                submitError = null;
                
                const result = await submitOnboarding(onboardingData);
                
                isCompleted = true;
                console.log('Onboarding completed with ID:', result.submission_id);
                
                // You could redirect to a success page or show a success message
                // For now, we'll just log it
                
            } catch (error) {
                submitError = error.message;
                console.error('Failed to submit onboarding:', error);
            } finally {
                isSubmitting = false;
            }
        } else {
            nextStep();
        }
    }

    $inspect(onboardingData);
</script>

<div class="onboarding-layout">
    <!-- Progress indicator -->
    <div class="progress-container">
        <div class="progress-header">
            <h3>Getting to know you</h3>
            <span class="step-counter">{currentStep} of {totalSteps}</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {(currentStep / totalSteps) * 100}%"></div>
        </div>
        <div class="progress-dots">
            {#each Array(totalSteps) as _, index}
                <button
                    class="progress-dot {index + 1 === currentStep ? 'active' : ''} {index + 1 < currentStep ? 'completed' : ''}"
                    onclick={() => goToStep(index + 1)}
                >
                    {#if index + 1 < currentStep}
                        ✓
                    {:else}
                        {index + 1}
                    {/if}
                </button>
            {/each}
        </div>
    </div>

    <div class="content-area">
        {#if isCompleted}
            <!-- Success message -->
            <div class="completion-message">
                <div class="success-icon">🎉</div>
                <h2>Welcome aboard!</h2>
                <p>Your onboarding has been completed successfully. We're excited to help you on your food journey!</p>
                <button class="get-started-button" onclick={() => window.location.href = '/meals'}>
                    Get Started
                </button>
            </div>
        {:else if currentStep === 1}
            <Step1 />
        {:else if currentStep === 2}
            <Step2 bind:selectedAllergies={onboardingData.allergies} />
        {:else if currentStep === 3}
            <Step3 bind:selectedNutritionGoals={onboardingData.nutrition_goals} />
        {:else if currentStep === 4}
            <Step4 bind:weeklyGroceryBudget={onboardingData.money_to_spend_per_week} />
        {:else if currentStep === 5}
            <Step5 bind:timeToCookPerDay={onboardingData.time_to_cook_per_day} />
        {:else if currentStep === 6}
            <Step6 bind:foodPreferences={onboardingData.food_preferences} />
        {:else if currentStep === 7}
            <Step7 bind:address={onboardingData.address} />
        {/if}
    </div>

    {#if !isCompleted}
        <div class="navigation-container">
            <button 
                class="nav-button secondary" 
                onclick={previousStep}
                disabled={currentStep === 1}
            >
                <span class="button-icon">←</span>
                Previous
            </button>

            <div class="nav-center">
                <span class="step-info">Step {currentStep} of {totalSteps}</span>
                {#if submitError}
                    <div class="error-message">{submitError}</div>
                {/if}
            </div>

            <button 
                class="nav-button primary" 
                onclick={handleComplete}
                disabled={isSubmitting}
            >
                {#if isSubmitting}
                    <span class="loading-spinner-small"></span>
                    Submitting...
                {:else if currentStep === totalSteps}
                    Complete
                {:else}
                    Next
                {/if}
                {#if !isSubmitting}
                    <span class="button-icon">→</span>
                {/if}
            </button>
        </div>
    {/if}
</div>

<style>
    .onboarding-layout {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
        max-width: 1200px;
        margin: 0 auto;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }

    .progress-container {
        background: white;
        padding: 2rem;
        border-bottom: 1px solid #e1e8ed;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }

    .progress-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }

    .progress-header h3 {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin: 0;
    }

    .step-counter {
        font-size: 1rem;
        color: #6c757d;
        font-weight: 500;
        background: #f8f9fa;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: 1px solid #e1e8ed;
    }

    .progress-bar {
        width: 100%;
        height: 6px;
        background: #e1e8ed;
        border-radius: 3px;
        overflow: hidden;
        margin-bottom: 1.5rem;
    }

    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #007bff, #28a745);
        border-radius: 3px;
        transition: width 0.3s ease;
    }

    .progress-dots {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 600px;
        margin: 0 auto;
    }

    .progress-dot {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        border: 2px solid #e1e8ed;
        background: white;
        color: #6c757d;
        font-size: 0.9rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .progress-dot:hover {
        border-color: #007bff;
        background: #e3f2fd;
    }

    .progress-dot.active {
        border-color: #007bff;
        background: #007bff;
        color: white;
        box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.2);
    }

    .progress-dot.completed {
        border-color: #28a745;
        background: #28a745;
        color: white;
    }

    .content-area {
        flex: 1;
        min-height: calc(100vh - 300px);
        overflow-y: auto;
        padding: 2rem;
        background: transparent;
    }

    .navigation-container {
        position: sticky;
        bottom: 0;
        background: white;
        border-top: 1px solid #e1e8ed;
        padding: 1.5rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 -2px 12px rgba(0, 0, 0, 0.08);
        z-index: 100;
    }

    .nav-button {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.875rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        border: 2px solid;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.2s ease;
        min-width: 140px;
        justify-content: center;
    }

    .nav-button.primary {
        background: linear-gradient(135deg, #007bff, #0056b3);
        border-color: #007bff;
        color: white;
    }

    .nav-button.primary:hover:not(:disabled) {
        background: linear-gradient(135deg, #0056b3, #004085);
        border-color: #0056b3;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
    }

    .nav-button.secondary {
        background: white;
        border-color: #6c757d;
        color: #6c757d;
    }

    .nav-button.secondary:hover:not(:disabled) {
        background: #f8f9fa;
        border-color: #495057;
        color: #495057;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    .nav-button:disabled {
        opacity: 0.4;
        cursor: not-allowed;
        transform: none;
    }

    .button-icon {
        font-size: 1.1rem;
        transition: transform 0.2s ease;
    }

    .nav-button:hover:not(:disabled) .button-icon {
        transform: translateX(2px);
    }

    .nav-button.secondary:hover:not(:disabled) .button-icon {
        transform: translateX(-2px);
    }

    .nav-center {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    .step-info {
        font-size: 0.9rem;
        color: #6c757d;
        font-weight: 500;
    }

    .completion-message {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 4rem 2rem;
        max-width: 600px;
        margin: 0 auto;
    }

    .success-icon {
        font-size: 4rem;
        margin-bottom: 2rem;
    }

    .completion-message h2 {
        font-size: 2.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }

    .completion-message p {
        font-size: 1.2rem;
        color: #6c757d;
        margin-bottom: 2rem;
        line-height: 1.6;
    }

    .get-started-button {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        border: none;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .get-started-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(40, 167, 69, 0.3);
    }

    .loading-spinner-small {
        display: inline-block;
        width: 16px;
        height: 16px;
        border: 2px solid transparent;
        border-top: 2px solid currentColor;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-right: 0.5rem;
    }

    .error-message {
        background: #fdf2f2;
        color: #dc2626;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.9rem;
        margin-top: 0.5rem;
        border: 1px solid #fecaca;
    }

    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    @media (max-width: 768px) {
        .progress-container {
            padding: 1.5rem 1rem;
        }
        
        .progress-header {
            flex-direction: column;
            gap: 1rem;
            align-items: flex-start;
        }
        
        .progress-dots {
            gap: 0.5rem;
        }
        
        .progress-dot {
            width: 35px;
            height: 35px;
            font-size: 0.8rem;
        }
        
        .content-area {
            padding: 1.5rem 1rem;
        }
        
        .navigation-container {
            padding: 1rem;
            flex-direction: column;
            gap: 1rem;
        }
        
        .nav-center {
            order: -1;
        }
        
        .nav-button {
            width: 100%;
            max-width: 300px;
        }
    }
</style>