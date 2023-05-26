<script>
	export let mode;
	let deckTitle = '';
	let deckDescription = '';
	let terms = [];
	let definitions = [];

	// Function to handle form submission
	function handleSubmit() {
		// Add your logic here to handle the form submission
	}
</script>

<main>
	<header>
		<h1>Edit Deck</h1>
		<div class="deck-info">
			<input type="text" bind:value={deckTitle} placeholder="Deck Title" class="input-field" />
			<textarea
				bind:value={deckDescription}
				placeholder="Deck Description"
				class="textarea-field"
			/>
		</div>
	</header>

	<!--   <div class="card-columns">
    <div class="term-column">
      <h2>Term</h2>
      <ul>
        {#each terms as term}
          <li>{term}</li>
        {/each}
      </ul>
    </div>
    <div class="definition-column">
      <h2>Definition</h2>
      <ul>
        {#each definitions as definition}
          <li>{definition}</li>
        {/each}
      </ul>
    </div>
  </div> -->

	<div class="button-container">
		<button class="button">Import</button>
		<span />
		<button class="button">Export</button>
	</div>

	<form on:submit|preventDefault={handleSubmit}>
		<div class="form-row">
			<input type="text" placeholder="Term" class="input-field" />
			<input type="text" placeholder="Definition" class="input-field" />
			<button class="button">Add Row</button>
		</div>
		<button class="button">Submit</button>
	</form>
	<button
		on:click={() => {
			mode = 'Slideshow';
		}}
		class="button">Back</button
	>
</main>

<style>
	main {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		background-color: #27374d;
		color: #ffffff;
		padding: 20px;
		height: 100vh;
		width: 100%;
	}

	header {
		text-align: center;
		margin-bottom: 20px;
	}

	.deck-info {
		display: flex;
		flex-direction: column;
		align-items: center;
		margin-bottom: 20px;
	}

	.input-field,
	.textarea-field {
		width: 100%;
		padding: 10px;
		margin-bottom: 10px;
		border-radius: 4px;
		border: none;
	}

	.textarea-field {
		height: 120px;
	}

	.card-columns {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
		grid-gap: 20px;
		margin-bottom: 20px;
	}

	.term-column,
	.definition-column {
		width: 100%;
	}

	.button-container {
		display: flex;
		flex-wrap: wrap;
		justify-content: space-between;
		margin-bottom: 20px;
	}

	.button {
		padding: 10px 20px;
		border-radius: 4px;
		border: none;
		background-color: #526d82;
		color: #ffffff;
		cursor: pointer;
	}

	.form-row {
		display: flex;
		align-items: center;
		justify-content: center;
		margin-bottom: 10px;
	}

	.form-row input[type='text'] {
		margin-right: 10px;
	}

	ul {
		list-style-type: none;
		padding: 0;
		margin: 0;
	}

	@media (max-width: 768px) {
		.card-columns {
			grid-template-columns: 1fr;
		}
	}
</style>
