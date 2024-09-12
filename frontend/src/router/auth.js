import { jwtDecode } from "jwt-decode"
import store from '../store'

export function isAuthenticated() {
  const token = localStorage.getItem('access_token');
  return !!token;
}

export function isTokenExpired(token) {
  if (!token) return true;

  const decoded = jwtDecode(token);
  const now = Date.now().valueOf() / 1000;

  return decoded.exp < now;
}

export function logout() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('userId');
  store.commit('SET_ACTIVE_CHAT', null)
}