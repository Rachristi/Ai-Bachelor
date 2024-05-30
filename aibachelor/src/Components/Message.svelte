<!-- Messages.svelte -->

<script lang="ts">
    import { afterUpdate, beforeUpdate } from "svelte";

	export let comments: { message: string; sender: string }[];
	export let isLoading: boolean;
	export let div: HTMLDivElement;
	export let autoscroll: boolean;

	// Adds a scroll event listener to the chat div
	beforeUpdate(() => {
		if (div) {
			const scrollableDistance = div.scrollHeight - div.offsetHeight;
			autoscroll = div.scrollTop >= scrollableDistance - 20;
		}
	});
	// Scrolls to the bottom of the chat div if autoscroll is true
	afterUpdate(() => {
		if (autoscroll && div) {
			div.scrollTop = div.scrollHeight;
		}
	});
</script>

<div class="chat" bind:this={div}>
	{#each comments as comment}
		<div class="message-container">
			<div class="message {comment.sender}">
				<article class={comment.sender}>
					{#if comment.sender === 'user'}
						<i class="fas fa-user"></i>
					{:else}
						<i class="fas fa-robot"></i>
					{/if}
					<span>{comment.message}</span>
				</article>
			</div>
		</div>
	{/each}
	{#if isLoading}
		<div class="spinner"></div>
	{/if}
</div>

<style>
	.chat {
		background-color: #f4f6f9;
		padding: 10px;
		border-radius: 10px;
		margin-bottom: 20px;
		overflow-y: auto;
		height: 300px; /* Limit chat height and add scrollbar */
		box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	.message-container {
		clear: both; /* Ensure each message starts on a new line */
		margin-bottom: 10px; /* Add some space between messages */
		display: flex;
	}

	.message {
		padding: 10px 15px;
		border-radius: 20px;
		max-width: 70%; /* Limit the width of the message box */
		word-wrap: break-word; /* Allow long messages to wrap */
		margin: 5px;
		font-size: 16px;
	}

	.user {
		background-color: #0074d9;
		color: white;
		align-self: flex-start;
        border-bottom-right-radius: 0;
		margin-right: 0;
		margin-left: auto; /* Align bot messages to the right */
	}
	.bot {
		background-color: #00c849;
		color: white;
		align-self: flex-end;
        border-bottom-left-radius: 0;
		margin-left: 0;
		margin-right: auto; /* Align user messages to the left */
	}

    .systemAlert{
		background-color: #ff0000;
		color: white;
		align-self: flex-end;
        border-bottom-left-radius: 0;
		margin-left: 0;
		margin-right: auto; /* Align user messages to the left */
    }

	.spinner {
		border: 4px solid #f3f3f3;
		border-top: 4px solid #3498db;
		border-radius: 50%;
		width: 24px;
		height: 24px;
		margin: 10px auto;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}
</style>
