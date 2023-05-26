<!-- App.svelte -->
<script>
	import { UserState } from '../../store.js';
	let email = '';
	let password = '';
	let signupEmail = '';
	let signupPassword = '';
	let isSignup = true;
	let displayName = '';
	const url = 'localhost:3000';

	let user = null;
	UserState.subscribe((value) => {
		$: user = value;
	});

	const API_KEY = 'AIzaSyDPoYA3017g0HwB1m0ZUUAxLKrbInm1fRg';
	async function handleLogin() {
		let url =
			'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=' + API_KEY;
		let body = JSON.stringify({ email, password, returnSecureToken: true });
		let res = await fetch(url, { method: 'POST', body });
		if (res.ok) {
			let data = await res.json();
			let temp_user = {
				displayName: data.displayName,
				email: data.email,
				idToken: data.idToken,
				refreshToken: data.refreshToken
			};
			UserState.update((state) => {
				return temp_user;
			});
		} else {
			alert('Cant make request');
		}
	}

	async function handleSignup() {
		let url = 'http://localhost:8000/v1/signup';
		let body = JSON.stringify({
			email: signupEmail,
			password: signupPassword,
			display_name: displayName
		});
		console.log(body);
		let res = await fetch(url, {
			method: 'POST',
			body: body,
			headers: {
				'Content-Type': 'application/json'
			}
		});
		console.log(res);
		if (res.ok) {
			alert('Signup Successfully! Please login');
		} else {
			alert('Invalid credentials');
		}
	}
</script>

{#if user == null}
	<main>
		{#if !isSignup}
			<h1>Login</h1>
			<form>
				<label>
					<span class="label-text">Email</span>
					<br />
					<input type="text" bind:value={email} class="input-field" />
				</label>
				<label>
					<span class="label-text">Password</span>
					<br />
					<input type="password" bind:value={password} class="input-field" />
				</label>
				<button on:click={handleLogin} class="button">Login</button>
			</form>
			<button
				on:click={() => {
					isSignup = true;
				}}
				style="margin-top:10px"
				class="button">New? Signup</button
			>
		{/if}
		{#if isSignup}
			<h1>Signup</h1>
			<form>
				<label>
					<span class="label-text">Email</span>
					<br />
					<input type="text" bind:value={signupEmail} class="input-field" />
				</label>
				<label>
					<span class="label-text">Password</span>
					<br />
					<input type="password" bind:value={signupPassword} class="input-field" />
				</label>
				<label>
					<span class="label-text">Display Name</span>
					<input type="text" bind:value={displayName} class="input-field" />
				</label>
				<button on:click={handleSignup} class="button">Signup</button>
			</form>
			<button
				on:click={() => {
					isSignup = false;
				}}
				style="margin-top:10px"
				class="button">To Signin</button
			>
		{/if}
	</main>
{/if}

<style>
	main {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100vh;
		background-color: #f5f5f5;
		padding: 2rem;
		padding-top: 0;
		width: 100%;
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
