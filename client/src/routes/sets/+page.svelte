<!-- App.svelte -->

<script>
	import { onMount, afterUpdate } from 'svelte';
	import Popup from '../statics/popup.svelte';
	import { APIUrl, UserState } from '../../store.js';

	export let mode;
	export let set_id;
	let showPopup = false;

	let decks = [{ set_name: 'deck1', set_id: 'asdasd' }];
	let user = null;
	UserState.subscribe((value) => (user = value));

	onMount(() => {
		fetchDecks();
	});

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

	async function addDeck(event) {
		let set_name = event.detail;
		if (user == null) {
			return;
		}
		const queryParams = {
			token: user.idToken
		};
		const queryString = new URLSearchParams(queryParams).toString();
		let url = APIUrl + '/v1/set' + '?' + queryString;
		let body = JSON.stringify({ set_name });
		let res = await fetch(url, {
			method: 'POST',
			body,
			headers: {
				'Content-Type': 'application/json'
			}
		});
		if (res.ok) {
			let _set = await res.json();
			decks.push(_set);
		} else {
			alert('Cant make request');
		}
	}
	onMount(() => {});
</script>

<div>
	{#if showPopup}
		<Popup on:accept={addDeck} bind:showPopup />
	{/if}
	{#if user != null}
		<div class="add-button">
			<div class="container">
				<button
					on:click={() => {
						showPopup = true;
					}}>Add Deck</button
				>
			</div>
			{#each decks as deck}
				<button
					on:click={() => {
						set_id = deck.set_id;
						mode = 'Home';
					}}
					class="deck"
				>
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
