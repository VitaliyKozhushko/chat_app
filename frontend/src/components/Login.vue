<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <el-button type="primary">Login</el-button>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import { io } from 'socket.io-client'

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: ''
    }
  },
  methods: {
    async login() {
      try {
        const response = await fetch('http://localhost:8000/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({
            username: this.username,
            password: this.password,
          }).toString(),
        });

        if (!response.ok) {
          throw new Error('Login failed');
        }

        const data = await response.json();
        const access_token = data.access_token
        this.socket = io("http://localhost:8000/", {
          query: {
            auth_token: access_token
          },
          transports: ["websocket"]
        });
        this.socket.on("connect", () => {
          console.log("Connected to WebSocket server!");
        });
        console.log('Login successful:', data);
      } catch (error) {
        this.errorMessage = 'Failed to log in. Please try again.';
        console.error('Error:', error);
      }
    },
  },
}
</script>

<style scoped>
.error {
  color: red;
}
</style>
