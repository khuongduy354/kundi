<!-- App.svelte -->
<script>
  let username = '';
  let password = '';
  let signupUsername = '';
  let signupPassword = '';

  function handleLogin() {
    // Handle login logic
    console.log("Login clicked");
    console.log("Username:", username);
    console.log("Password:", password);
  }

  function handleSignup() {
    // Handle signup logic
    console.log("Signup clicked");
    console.log("Username:", signupUsername);
    console.log("Password:", signupPassword);
  }
</script>

<main>
  <h1>Login</h1>
  <form>
    <label>
      <span class="label-text">Username</span>
      <input type="text" bind:value="{username}" class="input-field" />
    </label>
    <label>
      <span class="label-text">Password</span>
      <input type="password" bind:value="{password}" class="input-field" />
    </label>
    <button on:click="{handleLogin}" class="button">Login</button>
  </form>

  <h1>Signup</h1>
  <form>
    <label>
      <span class="label-text">Username</span>
      <input type="text" bind:value="{signupUsername}" class="input-field" />
    </label>
    <label>
      <span class="label-text">Password</span>
      <input type="password" bind:value="{signupPassword}" class="input-field" />
    </label>
    <button on:click="{handleSignup}" class="button">Signup</button>
  </form>
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background-color: #f5f5f5;
    padding: 2rem;
    padding-top:0;
    width:100%
  }

  h1 {
    margin-bottom: 1.5rem;
    color: #27374d;
    font-size: 24px;
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    max-width: 320px;
    width: 100%;
  }

  .label-text {
    font-size: 16px;
    color: #27374d;
    margin-bottom: 0.25rem;
  }

  .input-field {
    padding: 0.5rem;
    border-radius: 4px;
    border: 1px solid #ccc;
    font-size: 16px;
  }

  .button {
    padding: 0.5rem 1rem;
    background-color: #27374d;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
  }
</style>

