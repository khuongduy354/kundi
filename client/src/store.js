import { writable } from 'svelte/store';

export const UserState = writable({ displayName: 'Duy' });
export const APIUrl = 'http://localhost:8000';

// user = {
// 	displayName: data.displayName,
// 	email: data.email,
// 	idToken: data.idToken,
// 	refreshToken: data.refreshToken
// };
