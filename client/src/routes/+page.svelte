<script>
	import Edit from './statics/edit.svelte';
	import Slideshow from './statics/slideshow.svelte';
	import Login from './login/+page.svelte';
	import Sets from './sets/+page.svelte';
	export var mode = 'Home';
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

{#if mode == 'Slideshow' || mode == 'Home'}
	<Slideshow bind:mode />
{/if}

{#if mode == 'Edit'}
	<Edit bind:mode />
{/if}
{#if mode == 'Login'}
	<Login />
{/if}
{#if mode == 'Sets'}
	<Sets />
{/if}
