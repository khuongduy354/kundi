<!-- /* version two */ -->

<!-- FlashcardSlideshow.svelte -->

<script>
	import { onMount } from 'svelte';
	import { UserState, APIUrl } from '../../store.js';
	export let mode;
	export let set_id = '';
	export let set_name = 'Flashcard';

	let user = null;
	onMount(fetchCards);

	UserState.subscribe((value) => {
		user = value;
	});

	let currentIndex = 0;
	let frontHide = false;
	let backHide = true;
	function addFlashcard() {
		// Implement your logic to add a new flashcard
	}
	export let flashcards = [
		{ card_id: 'Term 1', word: 'word', definition: 'Definition 1' },
		{ card_id: 'asdfTerm 1', word: 'dasfafword', definition: 'Dasdfefinition 1' },
		{ card_id: 'Teradfm 1', word: 'wordasdf', definition: 'Definitadsfion 1' }
		// Add more flashcards as needed
	];

	async function fetchCards() {
		if (user == null || set_id == '') {
			return;
		}
		const queryParams = {
			token: user.idToken
		};
		const queryString = new URLSearchParams(queryParams).toString();
		let url = APIUrl + '/v1/sets/' + set_id + '/cards' + '?' + queryString;
		let res = await fetch(url);
		if (res.ok) {
			let temp = await res.json();
				flashcards = temp; 
        console.log(flashcards)
			
		} else {
			alert('Cant make request');
		}
	}
	function goToNextCard() {
		currentIndex = (currentIndex + 1) % flashcards.length;
		frontHide = false;
		backHide = true;
	}

	function goToPreviousCard() {
		currentIndex = (currentIndex - 1 + flashcards.length) % flashcards.length;
		backHide = true;
		frontHide = false;
	}

	function toggleFlip() {
		frontHide = !frontHide;
		backHide = !backHide;
	}
	let title = 'Flashcard Slideshow';
</script>

<main>
	<h1 class="KundiFl">Kundi Flashcard</h1>
	{#if user != null}
		<p>{set_name}</p>
		<div>{currentIndex + 1} / {flashcards.length}</div>
		<div class="flashcard-container">
			<div class="flashcard" on:click={toggleFlip}>
				<div class="front" class:hide={frontHide}>
					<h2>{flashcards[currentIndex].word}</h2>
				</div>
				<div class="back" class:hide={backHide}>
					<p>{flashcards[currentIndex].definition}</p>
				</div>
			</div>
		</div>

		<div class="controls">
			<div class="arrow" on:click={goToPreviousCard}>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 24 24"
					fill="#27374d"
					width="24px"
					height="24px"
				>
					<path d="M0 0h24v24H0z" fill="none" />
					<path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z" />
				</svg>
			</div>
			<div class="arrow" on:click={goToNextCard}>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 24 24"
					fill="#27374d"
					width="24px"
					height="24px"
				>
					<path d="M0 0h24v24H0z" fill="none" />
					<path d="M8.59 16.59L10 18l6-6-6-6-1.41 1.41L13.17 12z" />
				</svg>
			</div>
		</div>
		<div class="add-button">
			<button on:click={addFlashcard}>Shuffle</button>
		</div>
		<div class="add-button">
			<button on:click={addFlashcard}>Spaced Rep</button>
		</div>
		<div class="add-button">
			<button on:click={addFlashcard}>Quizzes</button>
		</div>

		<br />
		<br />
		<br />
		<br />

		<div class="add-button">
			<button
				on:click={() => {
					mode = 'Edit';
				}}>Add or remove terms</button
			>
		</div>
	{/if}
</main>

<style>
	main {
		display: flex;
		flex-direction: column;
		align-items: center;
		height: 100vh;
		background-color: #f0f2f5;
		padding: 2rem;
		width: 100vw;
	}
	.flashcard-container {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 300px;
	}

	.hide {
		visibility: hidden;
	}

	.flashcard {
		width: 300px;
		margin-bottom: 2rem;
		padding: 1.5rem;
		background-color: #ffffff;
		color: #000000;
		border-radius: 8px;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
		text-align: center;
		transform-style: preserve-3d;
		transition: transform 0.5s;
	}
	.title {
		text-align: center;
		font-size: 24px;
		margin-bottom: 1rem;
		color: #27374d;
	}

	.controls {
		display: flex;
		justify-content: center;
		gap: 1rem;
		margin-bottom: 1rem;
	}

	.arrow {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 40px;
		height: 40px;
		background-color: #ffffff;
		border: 1px solid #27374d;
		border-radius: 50%;
		cursor: pointer;
	}

	.arrow svg {
		width: 24px;
		height: 24px;
	}

	.add-button {
		display: flex;
		justify-content: center;
		margin-top: 1rem;
	}

	.add-button button {
		padding: 0.5rem 1rem;
		background-color: #27374d;
		color: #ffffff;
		border: none;
		border-radius: 4px;
		font-size: 16px;
		cursor: pointer;
	}
</style>
