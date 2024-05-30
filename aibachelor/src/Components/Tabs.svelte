<script lang="ts">
	export let activeTab: string;
	export let setActiveTab: (tab: string) => void;
</script>

<div class="tabs">
	<button class:active={activeTab === 'chat'} on:click={() => setActiveTab('chat')}>Chat</button>
	<button class:active={activeTab === 'settings'} on:click={() => setActiveTab('settings')}>Settings</button>
</div>

<style>
	.tabs {
		display: flex;
		justify-content: space-around;
		background-color: #f4f6f9;
		padding: 10px;
		border-bottom: 1px solid #ddd;
		border-radius: 10px 10px 0 0;
	}

	.tabs button {
		background: none;
		border: none;
		padding: 10px;
		cursor: pointer;
		transition: background-color 0.3s;
		outline: none;
	}

	.tabs button:hover,
	.tabs button.active {
		background-color: #ddd;
		border-radius: 5px;
	}
</style>
