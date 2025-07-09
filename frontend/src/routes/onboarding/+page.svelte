<script>
    import Step1 from "./Step1.svelte";
    import Step2 from "./Step2.svelte";
    import Step3 from "./Step3.svelte";
    import Step4 from "./Step4.svelte";
    import Step5 from "./Step5.svelte";
    import Step6 from "./Step6.svelte";
    import Step7 from "./Step7.svelte";

    let currentStep = $state(1);

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
</script>

{#if currentStep === 1}
    <Step1 />
{:else if currentStep === 2}
    <Step2 />
{:else if currentStep === 3}
    <Step3 />
{:else if currentStep === 4}
    <Step4 />
{:else if currentStep === 5}
    <Step5 />
{:else if currentStep === 6}
    <Step6 />
{:else if currentStep === 7}
    <Step7 />
{/if}

<div class="button-container">
    <button class="nav-button" onclick={() => currentStep--}>previous</button>
    <button class="nav-button" onclick={() => currentStep++}>next</button>
</div>

<style>
    .button-container {
        margin-top: 2rem;
        padding: 1rem;
        display: flex;
        justify-content: space-between;
        gap: 1rem;
    }

    .nav-button {
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border: 2px solid #007bff;
        border-radius: 8px;
        background-color: #007bff;
        color: white;
        cursor: pointer;
        transition: all 0.2s ease;
        min-width: 120px;
    }

    .nav-button:hover {
        background-color: #0056b3;
        border-color: #0056b3;
        transform: translateY(-1px);
    }

    .nav-button:active {
        transform: translateY(0);
    }
</style>