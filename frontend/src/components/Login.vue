<template>
  <div class="login-block">
    <el-input v-model="username" placeholder="username"/>
    <el-input v-model="password" placeholder="password"/>
    <el-button type="primary" class="login-btn" @click="login">Login</el-button>
    <el-button type="primary" @click="registration" link>Sign up?</el-button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { io } from 'socket.io-client'
import { defineEmits } from 'vue'

const emit = defineEmits(['displayRegistration']);

const registration = () => {
  emit('displayRegistration', true);
};

const notifyParent = () => {
  emit('updateParent', true); // Передаем значение родителю
};

const username = ref('');
const password = ref('');
const errorMessage = ref('');
let socket = null;

const login = async () => {
  try {
    const response = await fetch('http://localhost:8000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        username: username.value,
        password: password.value,
      }).toString(),
    });

    if (!response.ok) {
      throw new Error('Login failed');
    }

    const data = await response.json();
    const access_token = data.access_token;

    socket = io("http://localhost:8000/", {
      query: {
        auth_token: access_token
      },
      transports: ["websocket"]
    });

    socket.on("connect", () => {
      console.log("Connected to WebSocket server!");
    });

    console.log('Login successful:', data);
  } catch (error) {
    errorMessage.value = 'Failed to log in. Please try again.';
    console.error('Error:', error);
  }
}
</script>

<style scoped>
.error {
  color: red;
}
</style>
