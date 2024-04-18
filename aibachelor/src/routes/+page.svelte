<script lang="ts">

    let question: string = 'What is the answer?';
    let answer: string = '';
    let error: string = '';
    let methodarr: string[] = ['method1', 'method2', 'method3'];
    let method: string = '';
    let comments: any[] = [];
  
    async function sendQuestion() {
      try {
          comments = [...comments, question];
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
        const data = await response.json();
        answer = data.answer;
        comments = [...comments, answer];
        error = ''; // Clear any previous error
      } catch (err) {
        error = 'An error occurred while fetching data';
        console.error(err);
      }

    }


  </script>
  
  <div class="container">
    <div class="chat">
        <header>
            <h1>Chat Window</h1>
        </header>

        {#each comments as comment}
        <article class="article">
            <p>{comment}</p>
        </article>
            {/each}
    </div>
    <select bind:value={method}>
        {#each methodarr as m}
        <option value={m}>{m}</option>
        {/each}
    </select>What is the answer?
    <input bind:value={question} placeholder="Enter your question" />

    <div>
      <p>Question: {question}</p>
      <p>Answer: {answer}</p>
      <button on:click={sendQuestion}>Get Answer</button>
    </div>
    {#if error}
      <p>{error}</p>
    {/if}
  </div>

  <style>
    	.chat {
		height: 50%;
        width: 50%;
		flex: 1 1 auto;
		padding: 0 1em;
		overflow-y: auto;
		scroll-behavior: smooth;
	}
  </style>