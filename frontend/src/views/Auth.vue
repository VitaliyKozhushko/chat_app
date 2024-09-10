<template>
  <div class="auth-page">
    <div class="logo-block">
        <img class="logo" :src="logo" alt="logo">
      </div>
      <div v-if="!isLoginDisplay" class="sign-btns">
        <el-button type="primary" link @click="isLoginDisplay = !isLoginDisplay">Sign in</el-button>
        <el-button type="primary" link>Sign up</el-button>
      </div>
      <Login v-if="isLoginDisplay"/>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import logo from '@/assets/logo/logo.png'
import '@/assets/scss/auth.scss'
import Login from '@/components/Login.vue'


const isLoginDisplay = ref(false)
</script>