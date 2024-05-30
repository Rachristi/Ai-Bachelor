<!-- InputField.svelte -->
<script lang="ts">
	export let question: string;
	export let handleKeyDown: (event: KeyboardEvent & { currentTarget: EventTarget & HTMLInputElement }) => void;
	export let sendQuestion: () => void;
</script>

<div class="input-container">
	<input
		on:keydown={handleKeyDown}
		bind:value={question}
		placeholder="Enter your question"
	/>
	<button on:click={sendQuestion}>Submit question</button>
</div>

<style>
	.input-container {
		display: flex;
		align-items: center;
		justify-content: space-between;
		background-color: #f4f6f9;
		padding: 10px;
		border-top: 1px solid #ddd;
		border-radius: 0 0 10px 10px;
		box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.05);
	}

	.input-container input {
		flex: 1;
		padding: 10px;
		border: 1px solid #ccc;
		border-radius: 5px;
		margin-right: 10px;
	}

	.input-container button {
		padding: 10px 15px;
		background-color: #007bff;
		color: #fff;
		border: none;
		border-radius: 5px;
		cursor: pointer;
		transition: background-color 0.3s;
	}

	.input-container button:hover {
		background-color: #0056b3;
	}
</style>
