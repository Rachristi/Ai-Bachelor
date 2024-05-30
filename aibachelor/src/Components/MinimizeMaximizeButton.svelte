<!-- MinimizeMaximizeButton.svelte -->
<script lang="ts">
	export let isChatOpen: boolean;
	export let toggleChatOpen: () => void;
</script>

<button on:click={toggleChatOpen} class:is-minimized={!isChatOpen} class:is-maximized={isChatOpen}>
	{#if isChatOpen}
		<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
			<path d="M18 10H6V8h12v2zm-6 6H6v-2h6v2z" fill="currentColor"/>
		</svg>
	{:else}
		<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
			<path d="M6 10h12V8H6v2zm0 6h12v-2H6v2z" fill="currentColor"/>
		</svg>
	{/if}
</button>

<style>
	button {
		background: none;
		border: none;
		cursor: pointer;
		outline: none;
		padding: 10px;
		border-radius: 50%;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
		transition: background-color 0.3s, transform 0.3s, top 0.3s, right 0.3s;
		position: absolute;
	}

	button.is-maximized {
		top: 5px;
		right: 10px;
        background-color: rgb(148, 148, 148);
	}

	button.is-minimized {
		bottom: 10px;
		right: 10px;
		background-color: #007bff;
		transform: scale(1.2);
	}

	button svg {
		fill: #007bff;
		transition: fill 0.3s;
	}

	button.is-minimized svg {
		fill: white;
	}

	button:hover {
		background-color: rgba(0, 123, 255, 0.1);
	}

	button.is-minimized:hover {
		background-color: rgba(0, 123, 255, 0.2);
	}
</style>
