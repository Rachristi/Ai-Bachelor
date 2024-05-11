<script lang="ts">
    import { afterUpdate, beforeUpdate } from "svelte";
    import { flip } from "svelte/animate";


	let question: string = 'What is the answer?';
	let answer: string = '';
	let error: string = '';
	let methodarr: string[] = ['GPT2', 'BERT', 'GROQ'];
	let method: string = '';
	let comments: {message: string, sender: string}[] = [];
	let auther: string = 'user';
	let autoscroll: boolean = false;
	let div: HTMLDivElement;
	let isLoading: boolean = false;

	//Adds a scroll event listener to the chat div
	beforeUpdate(() => {
			if (div) {
				const scorllableDistance = div.scrollHeight - div.offsetHeight;
				autoscroll = div.scrollTop >= scorllableDistance - 20;
			}
		});
	//Scrolls to the bottom of the chat div if autoscroll is true
		afterUpdate(() => {
			if (autoscroll) {
				div.scrollTop = div.scrollHeight;
			}
		});
	
	function handleKeyPress(event: KeyboardEvent, ) {
		if (event.key === 'Enter') {
			sendQuestion();
		}
	}
	// Sends the question to the server and gets the answer
	async function sendQuestion() {
	isLoading = true;
	  try {
		auther = 'user';
		comments = [...comments, {message: question, sender: auther}];
		const response = await fetch('http://localhost:5000/answer', {  // Replace with your Flask server URL
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ question, method })
		});
		if (!response.ok) {
		  throw new Error('Failed to fetch data');
		}
		question = '';
		const data = await response.json();
		answer = data.answer;
		auther = data.sender;
		comments = [...comments, {message: answer, sender: auther}];
		error = ''; // Clear any previous error
	  } catch (err) {
		error = 'An error occurred while fetching data';
		console.error(err);
	  }
	  isLoading = false;
	}
</script>
  
  <div class="container">
	<div class="chat" bind:this={div}>
	  <header class="chat-header">
		<h1>Chat Window</h1>
	  </header>
  
	  {#each comments as comment }
	  <div class="message-container">
		<div class="message {comment.sender}">
			<article class="{comment.sender}">
				<span>{comment.message}</span>
			</article>
		</div>
	</div>
	{/each}
	{#if isLoading}
  		<div class="spinner"></div>
	{/if}
	</div>
  
	<div class="input-container">
	  <select bind:value={method}>
		{#each methodarr as m}
		<option value={m}>{m}</option>
		{/each}
	  </select>
	  <input on:keypress={handleKeyPress} bind:value={question} placeholder="Enter your question" />
	  <button on:click={sendQuestion}>Get Answer</button>
	</div>
</div>  

  <style>
    .container {
        max-width: 600px;
        margin: 0 auto;
        padding: 20px;
        border: 1px solid #cccccc;
        border-radius: 5px;
    }

    .chat {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 20px;
        overflow-y: auto;
        height: 300px; /* Limit chat height and add scrollbar */
    }

    .chat-header {
        text-align: center;
        margin-bottom: 20px;
    }

    .message-container {
        clear: both; /* Ensure each message starts on a new line */
        margin-bottom: 10px; /* Add some space between messages */
    }

    .message {
        padding: 5px 10px;
        border-radius: 10px;
        max-width: 70%; /* Limit the width of the message box */
        word-wrap: break-word; /* Allow long messages to wrap */
    }

    .user {
        background-color: #0074d9;
        color: white;
        float: right; /* Align user messages to the right */
    }

    .bot {
        background-color: rgb(0, 200, 73);
        color: white;
        float: left; /* Align bot messages to the left */
    }
  .input-container {
	display: flex;
	align-items: center;
	margin-bottom: 20px;
  }

  .input-container input {
	flex: 1;
	padding: 10px;
	border: 1px solid #ccc;
	border-radius: 5px;
  }

  .input-container button {
	padding: 10px 20px;
	background-color: #007bff;
	color: #fff;
	border: none;
	border-radius: 5px;
	cursor: pointer;
  }

  .spinner {
    border: 16px solid #f3f3f3;
    border-radius: 50%;
    border-top: 16px solid #3498db;
    width: 30px;
    height: 30px;
    animation: spin 2s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
</style>