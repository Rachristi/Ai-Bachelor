<script lang="ts">
	import { afterUpdate, beforeUpdate } from "svelte";
	import { ApiHelper } from "../Helper/ApiHelper";
	import Message from "../Components/Message.svelte";
	import MinimizeMaximizeButton from "../Components/MinimizeMaximizeButton.svelte";
	import Tabs from "../Components/Tabs.svelte";
	import Settings from "../Components/Settings.svelte";
    import InputField from "../Components/InputField.svelte";
    import { sanitizeInput } from "../Helper/InputSanitizeHelper";

	let question: string = "";
	let error: string = "";
	let answer: string = "";
	let methodarr: string[] = [
		"GROG",
		"LLAMA",
		"LLAMANOCONTEXT",
		"MIXTRAL",
		"MIXTRALNOCONTEXT",
		"GOOGLE",
		"GOOGLENOCONTEXT",
	];
	let method: string = "";
	let comments: { message: string; sender: string }[] = [];
	let auther: string = "user";
	let autoscroll: boolean = false;
	let div: HTMLDivElement;
	let isLoading = false;
	let isChatOpen = true;
	let activeTab = "chat";

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

	// Sends the question to the server and gets the answer
	async function sendQuestion() {
		try {
			const sanitizedQuestion = sanitizeInput(question);
			comments = [...comments, { message: question, sender: "user" }];
			isLoading = true;
			const response = await ApiHelper.sendQuestion(sanitizedQuestion, method, comments, auther);
			comments = response.comments;
			error = response.error;
			isLoading = response.isLoading;
			question = response.question;
		} catch (err) {
			// Handle validation errors or sanitization errors
			answer = (err as Error).message;
			auther = "systemAlert";
			comments = [...comments, { message: answer, sender: auther }];
			error = "An error occurred while processing the input";
			console.error(err);
			isLoading = false;
		}
	}

	function handleKeyDown(
		event: KeyboardEvent & {
			currentTarget: EventTarget & HTMLInputElement;
		},
	) {
		if (event.key === "Enter") {
			sendQuestion();
		}
	}

	
	function toggleChatOpen() {
		isChatOpen = !isChatOpen;
	}

	function setActiveTab(tab: string) {
		activeTab = tab;
	}

	async function createEmbeddings(
		event: MouseEvent & { currentTarget: EventTarget & HTMLButtonElement },
	) {
		try {
			await ApiHelper.createEmbeddings();
		} catch (err) {
			error = "An error occurred while fetching data";
			console.error(err);
		}
	}
</script>

<div class="chat-window">
	<MinimizeMaximizeButton {isChatOpen} {toggleChatOpen}/>

	<div class="chat-container {isChatOpen ? '' : 'hidden'}">
		<Tabs {activeTab} {setActiveTab}/>
		<div class="tab-content">
			{#if activeTab === "chat"}
				<div class="container">
					<Message {comments} {isLoading} bind:div={div} bind:autoscroll={autoscroll} />
					<InputField bind:question={question} {handleKeyDown} {sendQuestion}/>
				</div>
			{:else if activeTab === "settings"}
				<div class="container">
					<Settings bind:method={method} {methodarr} {createEmbeddings} />
				</div>
			{/if}
		</div>
	</div>
</div>

<style>
	.chat-window {
		position: fixed;
		bottom: 0;
		right: 0;
		width: 400px;
		background-color: #fff;
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
		border-radius: 10px 10px 0 0;
		font-family: "Arial", sans-serif;
	}

	.hidden {
		display: none;
	}

	.container {
		max-height: 500px;
		overflow-y: auto;
		max-width: 380px;
		margin: 0 auto;
		padding: 10px 20px 20px 20px;
		border-radius: 0 0 10px 10px;
	}
		
</style>
