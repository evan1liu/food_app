<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    
    // Props - bind to parent's address data
    let { address = $bindable() } = $props();
    
    // Component state
    let searchInput: HTMLInputElement;
    let searchValue = $state('');
    let suggestions = $state<any[]>([]);
    let isLoading = $state(false);
    let isAPILoaded = $state(false);
    let loadError = $state<string | null>(null);
    let showSuggestions = $state(false);
    let selectedIndex = $state(-1);
    let debounceTimer: number | null = null;
    
    // Address components state
    let selectedPlace = $state<any>(null);
    let addressComponents = $state({
        streetNumber: '',
        route: '',
        locality: '',
        administrativeAreaLevel1: '',
        country: '',
        postalCode: '',
        formattedAddress: '',
        placeId: '',
        geometry: null as { lat: number; lng: number } | null
    });

    // Google Maps API configuration
    const GOOGLE_API_KEY = "AIzaSyDmB4a-IqjydURr8CyAEkcZ8s0gCh7kZB0";
    const GOOGLE_MAPS_SCRIPT_ID = 'google-maps-script-new';

    // Load Google Maps JavaScript API with Places library (New)
    async function loadGoogleMapsScript(): Promise<void> {
        return new Promise((resolve, reject) => {
            // Check if Google Maps is already loaded
            if (window.google && window.google.maps) {
                resolve();
                return;
            }

            // Check if script is already being loaded
            if (document.getElementById(GOOGLE_MAPS_SCRIPT_ID)) {
                const existingScript = document.getElementById(GOOGLE_MAPS_SCRIPT_ID) as HTMLScriptElement;
                existingScript.onload = () => resolve();
                existingScript.onerror = () => reject(new Error('Failed to load Google Maps script'));
                return;
            }

            // Create and load the script
            const script = document.createElement('script');
            script.id = GOOGLE_MAPS_SCRIPT_ID;
            script.src = `https://maps.googleapis.com/maps/api/js?key=${GOOGLE_API_KEY}&libraries=places&loading=async`;
            script.async = true;
            script.defer = true;
            
            script.onload = () => resolve();
            script.onerror = () => reject(new Error('Failed to load Google Maps script'));

            document.head.appendChild(script);
        });
    }

    // Search for place suggestions using the new AutocompleteSuggestion API
    async function searchPlaces(query: string) {
        if (!query || query.length < 2 || !isAPILoaded) {
            suggestions = [];
            showSuggestions = false;
            return;
        }

        try {
            isLoading = true;
            loadError = null;

            // Load the places library
            const { AutocompleteSuggestion } = await google.maps.importLibrary('places') as google.maps.PlacesLibrary;

            // Fetch autocomplete suggestions using the new API
            const { suggestions: placeSuggestions } = await AutocompleteSuggestion.fetchAutocompleteSuggestions({
                input: query,
                // Restrict results to US addresses only
                includedRegionCodes: ['us'],
            });

            // Process suggestions
            suggestions = placeSuggestions.map((suggestion: any) => {
                const prediction = suggestion.placePrediction;
                return {
                    placeId: prediction.placeId,
                    description: `${prediction.mainText.text}, ${prediction.secondaryText.text}`,
                    mainText: prediction.mainText.text,
                    secondaryText: prediction.secondaryText.text,
                    types: prediction.types || []
                };
            });

            showSuggestions = suggestions.length > 0;
            selectedIndex = -1;

        } catch (error) {
            console.error('Error fetching place suggestions:', error);
            loadError = 'Failed to fetch suggestions';
            suggestions = [];
            showSuggestions = false;
        } finally {
            isLoading = false;
        }
    }

    // Get place details using the new Place Details API
    async function getPlaceDetails(placeId: string) {
        try {
            // Load the places library
            const { Place } = await google.maps.importLibrary('places') as google.maps.PlacesLibrary;

            // Create a place request
            const place = new Place({
                id: placeId,
                requestedLanguage: 'en'
            });

            // Fetch place details
            await place.fetchFields({
                fields: [
                    'addressComponents',
                    'formattedAddress',
                    'location',
                    'id'
                ]
            });

            return place;
        } catch (error) {
            console.error('Error fetching place details:', error);
            throw error;
        }
    }

    // Handle suggestion selection
    async function selectSuggestion(suggestion: any) {
        try {
            isLoading = true;
            searchValue = suggestion.description;
            showSuggestions = false;

            // Get detailed place information
            const place = await getPlaceDetails(suggestion.placeId);
            
            // Parse address components
            parseAddressComponents(place);
            
        } catch (error) {
            console.error('Error selecting place:', error);
            loadError = 'Failed to get place details';
        } finally {
            isLoading = false;
        }
    }

    // Parse place details into address components
    function parseAddressComponents(place: any) {
        const components = place.addressComponents || [];
        
        // Create a map for easy lookup
        const componentMap: Record<string, string> = {};
        
        for (const component of components) {
            const componentType = component.types[0];
            componentMap[componentType] = component.longText;
        }

        // Extract and set address components
        addressComponents = {
            streetNumber: componentMap['street_number'] || '',
            route: componentMap['route'] || '',
            locality: componentMap['locality'] || componentMap['administrative_area_level_2'] || '',
            administrativeAreaLevel1: componentMap['administrative_area_level_1'] || '',
            country: componentMap['country'] || '',
            postalCode: componentMap['postal_code'] || '',
            formattedAddress: place.formattedAddress || '',
            placeId: place.id || '',
            geometry: place.location ? {
                lat: place.location.lat(),
                lng: place.location.lng()
            } : null
        };

        // Update the bound address prop
        address = addressComponents.formattedAddress;
        selectedPlace = place;
        
        console.log('Selected place details:', addressComponents);
    }

    // Handle input changes with debouncing
    function handleInputChange() {
        // Clear previous timer
        if (debounceTimer) {
            clearTimeout(debounceTimer);
        }

        // Set new timer
        debounceTimer = setTimeout(() => {
            searchPlaces(searchValue);
        }, 300);

        // If input is cleared, reset everything
        if (!searchValue) {
            resetAddressComponents();
        }
    }

    // Handle keyboard navigation
    function handleKeyDown(event: KeyboardEvent) {
        if (!showSuggestions || suggestions.length === 0) return;

        switch (event.key) {
            case 'ArrowDown':
                event.preventDefault();
                selectedIndex = selectedIndex < suggestions.length - 1 ? selectedIndex + 1 : 0;
                break;
            case 'ArrowUp':
                event.preventDefault();
                selectedIndex = selectedIndex > 0 ? selectedIndex - 1 : suggestions.length - 1;
                break;
            case 'Enter':
                event.preventDefault();
                if (selectedIndex >= 0 && selectedIndex < suggestions.length) {
                    selectSuggestion(suggestions[selectedIndex]);
                }
                break;
            case 'Escape':
                showSuggestions = false;
                selectedIndex = -1;
                break;
        }
    }

    // Reset address components
    function resetAddressComponents() {
        addressComponents = {
            streetNumber: '',
            route: '',
            locality: '',
            administrativeAreaLevel1: '',
            country: '',
            postalCode: '',
            formattedAddress: '',
            placeId: '',
            geometry: null
        };
        address = '';
        selectedPlace = null;
    }

    // Clear search
    function clearSearch() {
        searchValue = '';
        suggestions = [];
        showSuggestions = false;
        resetAddressComponents();
        searchInput?.focus();
    }

    // Component lifecycle
    onMount(async () => {
        try {
            loadError = null;
            await loadGoogleMapsScript();
            isAPILoaded = true;
            console.log('Google Maps API (New) loaded successfully');
        } catch (error) {
            console.error('Error loading Google Maps:', error);
            loadError = error instanceof Error ? error.message : 'Failed to load Google Maps';
        }
    });

    onDestroy(() => {
        if (debounceTimer) {
            clearTimeout(debounceTimer);
        }
    });

    // Set initial value if address prop is provided
    $effect(() => {
        if (address && !selectedPlace) {
            searchValue = address;
        }
    });

    // Hide suggestions when clicking outside
    function handleClickOutside(event: Event) {
        const target = event.target as HTMLElement;
        if (!target.closest('.autocomplete-container')) {
            showSuggestions = false;
            selectedIndex = -1;
        }
    }

    onMount(() => {
        document.addEventListener('click', handleClickOutside);
        return () => document.removeEventListener('click', handleClickOutside);
    });
</script>

<div class="address-step">
    <h2>What's your address?</h2>
    <p class="subtitle">We'll use this to find the best grocery stores and delivery options near you.</p>
    
    <div class="autocomplete-container">
        <label for="address-input" class="input-label">
            Street Address
        </label>
        
        <div class="input-wrapper">
            <input
                bind:this={searchInput}
                bind:value={searchValue}
                id="address-input"
                type="text"
                class="address-input"
                placeholder="Start typing your address..."
                disabled={!isAPILoaded || !!loadError}
                oninput={handleInputChange}
                onkeydown={handleKeyDown}
                autocomplete="off"
            />
            
            {#if searchValue && !isLoading}
                <button 
                    class="clear-button"
                    onclick={clearSearch}
                    title="Clear search"
                >
                    ✕
                </button>
            {/if}
            
            {#if isLoading}
                <div class="loading-spinner"></div>
            {/if}
        </div>

        <!-- Suggestions dropdown -->
        {#if showSuggestions && suggestions.length > 0}
            <div class="suggestions-dropdown">
                {#each suggestions as suggestion, index}
                    <button
                        class="suggestion-item {selectedIndex === index ? 'selected' : ''}"
                        onclick={() => selectSuggestion(suggestion)}
                    >
                        <div class="suggestion-main">{suggestion.mainText}</div>
                        <div class="suggestion-secondary">{suggestion.secondaryText}</div>
                    </button>
                {/each}
            </div>
        {/if}

        {#if !isAPILoaded && !loadError}
            <div class="info-message">
                <small>Loading Google Maps...</small>
            </div>
        {/if}
        
        {#if loadError}
            <div class="error-message">
                <strong>Error:</strong> {loadError}
                <br>
                <small>You can still enter your address manually, but autocomplete won't be available.</small>
            </div>
        {/if}
    </div>

    <!-- Address confirmation -->
    {#if selectedPlace && addressComponents.formattedAddress}
        <div class="address-confirmation">
            <h4>📍 Selected Address:</h4>
            <p class="selected-address">{addressComponents.formattedAddress}</p>
            <button 
                class="change-button" 
                onclick={clearSearch}
            >
                Change address
            </button>
        </div>
    {/if}

    <!-- Debug info (development only) -->
    {#if addressComponents.formattedAddress && import.meta.env.DEV}
        <div class="debug-info">
            <h4>Address Components (Debug Info):</h4>
            <ul>
                <li><strong>Full Address:</strong> {addressComponents.formattedAddress}</li>
                <li><strong>Street:</strong> {addressComponents.streetNumber} {addressComponents.route}</li>
                <li><strong>City:</strong> {addressComponents.locality}</li>
                <li><strong>State/Province:</strong> {addressComponents.administrativeAreaLevel1}</li>
                <li><strong>Country:</strong> {addressComponents.country}</li>
                <li><strong>Postal Code:</strong> {addressComponents.postalCode}</li>
                <li><strong>Place ID:</strong> {addressComponents.placeId}</li>
                {#if addressComponents.geometry}
                    <li><strong>Coordinates:</strong> {addressComponents.geometry.lat}, {addressComponents.geometry.lng}</li>
                {/if}
            </ul>
        </div>
    {/if}
</div>

<style>
    .address-step {
        max-width: 600px;
        margin: 0 auto;
        padding: 2rem;
    }

    h2 {
        color: #2c3e50;
        margin-bottom: 0.5rem;
        font-size: 2rem;
        font-weight: 600;
    }

    .subtitle {
        color: #7f8c8d;
        margin-bottom: 2rem;
        font-size: 1.1rem;
        line-height: 1.5;
    }

    .autocomplete-container {
        position: relative;
        margin-bottom: 1.5rem;
    }

    .input-label {
        display: block;
        margin-bottom: 0.5rem;
        color: #34495e;
        font-weight: 500;
        font-size: 1rem;
    }

    .input-wrapper {
        position: relative;
        display: flex;
        align-items: center;
    }

    .address-input {
        width: 100%;
        padding: 1rem;
        padding-right: 3rem;
        font-size: 1.1rem;
        border: 2px solid #e1e8ed;
        border-radius: 8px;
        background-color: white;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
        box-sizing: border-box;
    }

    .address-input:focus {
        outline: none;
        border-color: #3498db;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
    }

    .address-input:disabled {
        background-color: #f8f9fa;
        color: #6c757d;
        cursor: not-allowed;
    }

    .clear-button {
        position: absolute;
        right: 12px;
        background: none;
        border: none;
        font-size: 1.2rem;
        color: #9ca3af;
        cursor: pointer;
        padding: 4px;
        border-radius: 4px;
        transition: color 0.2s ease;
    }

    .clear-button:hover {
        color: #6b7280;
        background-color: #f3f4f6;
    }

    .loading-spinner {
        position: absolute;
        right: 12px;
        width: 20px;
        height: 20px;
        border: 2px solid #e1e8ed;
        border-top: 2px solid #3498db;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    .suggestions-dropdown {
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: white;
        border: 1px solid #e1e8ed;
        border-radius: 8px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        max-height: 300px;
        overflow-y: auto;
    }

    .suggestion-item {
        display: block;
        width: 100%;
        padding: 12px 16px;
        border: none;
        background: none;
        text-align: left;
        cursor: pointer;
        border-bottom: 1px solid #f1f3f4;
        transition: background-color 0.2s ease;
    }

    .suggestion-item:hover,
    .suggestion-item.selected {
        background-color: #f8f9fa;
    }

    .suggestion-item.selected {
        background-color: #e3f2fd;
    }

    .suggestion-main {
        font-weight: 500;
        color: #2c3e50;
        margin-bottom: 2px;
    }

    .suggestion-secondary {
        font-size: 0.9rem;
        color: #7f8c8d;
    }

    .info-message {
        margin-top: 0.5rem;
        color: #6b7280;
        font-size: 0.9rem;
    }

    .error-message {
        margin-top: 0.5rem;
        padding: 0.75rem;
        background-color: #fdf2f2;
        border: 1px solid #fecaca;
        border-radius: 6px;
        color: #dc2626;
        font-size: 0.9rem;
    }

    .address-confirmation {
        background-color: #f0f9ff;
        border: 1px solid #bae6fd;
        border-radius: 8px;
        padding: 1.5rem;
        margin-top: 1.5rem;
    }

    .address-confirmation h4 {
        margin: 0 0 0.75rem 0;
        color: #0369a1;
        font-size: 1.1rem;
    }

    .selected-address {
        margin: 0 0 1rem 0;
        font-size: 1.1rem;
        font-weight: 500;
        color: #374151;
        line-height: 1.5;
    }

    .change-button {
        background-color: white;
        border: 1px solid #d1d5db;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
        color: #6b7280;
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .change-button:hover {
        background-color: #f9fafb;
        border-color: #9ca3af;
        color: #374151;
    }

    .debug-info {
        margin-top: 2rem;
        padding: 1rem;
        background-color: #f3f4f6;
        border-radius: 6px;
        font-size: 0.85rem;
    }

    .debug-info h4 {
        margin: 0 0 0.75rem 0;
        color: #6b7280;
    }

    .debug-info ul {
        margin: 0;
        padding-left: 1rem;
    }

    .debug-info li {
        margin-bottom: 0.25rem;
        color: #4b5563;
    }
</style>
