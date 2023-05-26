<script>
	import Header from './Header.svelte';
	import Home from './+page.svelte';
	let mode = 'Home';
</script>

<div class="app">
	<Header bind:mode />

	<main>
		<Home bind:mode />
	</main>
</div>

<style>
</style>
