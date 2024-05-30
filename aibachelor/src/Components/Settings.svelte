<script lang="ts">
    export let method: String;
    export let methodarr: String[];
    export let createEmbeddings: (event: MouseEvent & { currentTarget: EventTarget & HTMLButtonElement }) => void;

</script>

<div class="settings">
    <select bind:value={method}>
        {#each methodarr as m}
            <option value={m}>{m}</option>
        {/each}
    </select>
    <button on:click={createEmbeddings}
        >Create Embeddings</button
    >
</div>

<style>
    .settings {
		display: flex;
		flex-direction: column;
		gap: 10px;
	}

	.settings select,
	.settings button {
		padding: 10px;
		border: 1px solid #ccc;
		border-radius: 5px;
		cursor: pointer;
		transition: background-color 0.3s;
	}

	.settings button {
		background-color: #007bff;
		color: white;
	}

	.settings button:hover {
		background-color: #0056b3;
	}
</style>