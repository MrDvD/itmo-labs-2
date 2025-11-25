import type { ClientState } from "@lib/dto.js";
import { writable } from "svelte/store";

export const CLIENT_STATE = writable<ClientState>({
  isAuthorized: false,
  login: "",
});

export function getCookie(name: string): string | null {
	const nameLenPlus = (name.length + 1);
	return document.cookie
		.split(';')
		.map(c => c.trim())
		.filter(cookie => {
			return cookie.substring(0, nameLenPlus) === `${name}=`;
		})
		.map(cookie => {
			return decodeURIComponent(cookie.substring(nameLenPlus));
		})[0] || null;
}