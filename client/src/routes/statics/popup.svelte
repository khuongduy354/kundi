<!-- PopupPrompt.svelte -->
<script>
  import { createEventDispatcher } from 'svelte';

  let inputValue = '';
  let isOpen = true;

  const dispatch = createEventDispatcher();

  function openPrompt() {
    isOpen = true;
  }

  function closePrompt() {
    isOpen = false;
  }

  function handleAccept() {
    dispatch('accept', inputValue);
    closePrompt();
  }

  function handleReject() {
    dispatch('reject');
    closePrompt();
  }
</script>

{#if isOpen}
  <div class="overlay">
    <div class="prompt">
			<p>
				You gonna create a new set <br> please add a name to it
			</p>
      <input type="text" bind:value="{inputValue}"  />

      <div class="buttons">
        <button on:click="{handleAccept}">Accept</button>
        <button on:click="{handleReject}">Reject</button>
      </div>
    </div>
  </div>
{/if}
<!-- PopupPrompt.svelte -->
<!-- PopupPrompt.svelte -->
<!-- PopupPrompt.svelte -->
<style>
  .overlay {
    /* Overlay styles */
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .prompt {
    /* Prompt styles */
    background-color: #27374D;
    padding: 16px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  input[type="text"] {
    /* Input styles */
    width: 100%;
    padding: 8px;
    border: 1px solid #526D82;
    border-radius: 4px;
    margin-bottom: 16px;
    color: #FFFFFF;
    background-color: #526D82;
  }

  .buttons {
    /* Button styles */
    display: flex;
    justify-content: center;
  }

  button {
    /* Button styles */
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    margin-right: 8px;
    cursor: pointer;
    color: #27374D;
  }

  .accept {
    /* Accept button styles */
    background-color: #9DB2BF;
  }

  .reject {
    /* Reject button styles */
    background-color: #DDE6ED;
    color: #27374D;
  }

  h2 {
    /* Title styles */
    color: #27374D;
    font-size: 24px;
    margin-bottom: 16px;
  }

  p {
    /* Text styles */
    color: #ffffff;
    font-size: 16px;
    margin-bottom: 16px;
  }
</style>



