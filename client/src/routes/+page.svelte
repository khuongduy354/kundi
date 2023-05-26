<script>
	import Edit from './statics/edit.svelte';
	import Slideshow from './statics/slideshow.svelte';
	import Login from './login/+page.svelte';
	import Sets from './sets/+page.svelte';
	export var mode = 'Home';
	let set_id = '';
	let set_name = '';
	let flashcards = [
		{ card_id: 'Term 1', word: 'word', definition: 'Definition 1' },
		{ card_id: 'asdfTerm 1', word: 'dasfafword', definition: 'Dasdfefinition 1' },
		{ card_id: 'Teradfm 1', word: 'wordasdf', definition: 'Definitadsfion 1' }
	];
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

{#if mode == 'Slideshow' || mode == 'Home'}
	<Slideshow bind:set_id bind:mode bind:flashcards />
{/if}

{#if mode == 'Edit'}
	<Edit bind:mode bind:set_name bind:flashcards />
{/if}
{#if mode == 'Login'}
	<Login />
{/if}
{#if mode == 'Sets'}
	<Sets bind:set_id bind:mode bind:set_name />
{/if}
