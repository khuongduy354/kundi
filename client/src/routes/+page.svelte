<script>
	import Edit from './statics/edit.svelte';
	import Slideshow from './statics/slideshow.svelte';
	import Login from './login/+page.svelte';
	import Sets from './sets/+page.svelte';
	export var mode = 'Home';
	let set_id = '';
	let set_name = '';
	let flashcards = [{ card_id: '', word: '', definition: '' }];
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

{#if mode == 'Slideshow' || mode == 'Home'}
	<Slideshow bind:set_id bind:mode bind:flashcards bind:set_name />
{/if}

{#if mode == 'Edit'}
	<Edit bind:mode bind:set_name bind:flashcards bind:set_id />
{/if}
{#if mode == 'Login'}
	<Login />
{/if}
{#if mode == 'Sets'}
	<Sets bind:set_id bind:mode bind:set_name />
{/if}
