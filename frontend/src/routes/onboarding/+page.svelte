<script>
    import Step1 from "./Step1.svelte";
    import Step2 from "./Step2.svelte";
    import Step3 from "./Step3.svelte";
    import Step4 from "./Step4.svelte";
    import Step5 from "./Step5.svelte";
    import Step6 from "./Step6.svelte";
    import Step7 from "./Step7.svelte";

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

<Step1 />