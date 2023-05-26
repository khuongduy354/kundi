<!-- App.svelte -->

<script>
	import { onMount } from 'svelte';
	import { APIUrl, UserState } from '../../store.js';

	let decks = [{ set_name: 'deck1', set_id: 'asdasd' }];
	function addDeck() {}
	let user = null;
	UserState.subscribe((value) => (user = value));

	onMount(fetchDecks);
	async function fetchDecks() {
		if (user == null) {
			return;
		}
		const queryParams = {
			token: user.idToken
		};
		const queryString = new URLSearchParams(queryParams).toString();
		let url = APIUrl + '/v1/sets' + '?' + queryString;
		let res = await fetch(url);
		if (res.ok) {
			decks = await res.json();
		} else {
			alert('Cant make request');
		}
	}
</script>

<div>
	{#if user != null}
		<div class="add-button">
			<div class="container">
				<button on:click={addDeck}>Add Deck</button>
			</div>
			{#each decks as deck}
				<button class="deck">
					<h2>{deck.set_name}</h2>
				</button>
			{/each}
		</div>
	{/if}
</div>

<style>
	:root {
		--primary-color: #ffffff;
		--secondary-color: #526d82;
		--accent-color: #9db2bf;
		--background-color: #dde6ed;
	}

	body {
		background-color: var(--background-color);
		font-family: sans-serif;
		margin: 0;
		padding: 0;
	}

	.container {
		display: flex;
		flex-wrap: wrap;
		justify-content: left;
		padding: 50px;
	}

	.deck {
		background-color: var(--secondary-color);
		border: none;
		border-radius: 10px;
		height: 150px;
		margin: 20px;
		transition: all 0.2s ease-in-out;
		width: 150px;
	}

	.deck:hover {
		box-shadow: 0px 0px 10px var(--primary-color);
		transform: translateY(-5px);
	}

	.deck h2 {
		color: var(--primary-color);
		font-size: 1.5rem;
		margin: 0;
		padding: 20px;
		text-align: center;
	}

	.add-button {
		display: block;
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
