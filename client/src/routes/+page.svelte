<script>
import Edit from "./statics/edit.svelte" 
import Slideshow from "./statics/slideshow.svelte"
let showSlide = true  
</script>

<svelte:head> 
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head> 

{#if showSlide}
<Slideshow bind:showSlide/>
{/if} 

{#if !showSlide}
<Edit bind:showSlide />
{/if}
 


