<script setup>
import logo from '@/assets/logo/logo.png'
import '@/assets/scss/auth.scss'
</script>

<template>
  <div class="auth-page">
    <div class="logo-block">
        <img class="logo" :src="logo" alt="logo">
      </div>
      <div class="sign-btns">
        <el-button type="primary" link>Sign in</el-button>
        <el-button type="primary" link>Sign up</el-button>
      </div>
  </div>
</template>