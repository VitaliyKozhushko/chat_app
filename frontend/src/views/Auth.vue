<template>
  <div class="auth-page">
    <div class="logo-block">
        <img class="logo" :src="logo" alt="logo">
      </div>
      <div v-if="!isLoginDisplay && !isRegisterDisplay" class="sign-btns">
        <el-button type="primary" link @click="isLoginDisplay = !isLoginDisplay">Sign in</el-button>
        <el-button type="primary" link @click="isRegisterDisplay = !isRegisterDisplay">Sign up</el-button>
      </div>
      <Login v-if="isLoginDisplay" @displayRegistration="displayReg"/>
      <Registration v-if="isRegisterDisplay"/>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import logo from '@/assets/logo/logo.png'
import '@/assets/scss/auth.scss'
import Login from '@/components/Login.vue'
import Registration from '@/components/Registration.vue'


const isLoginDisplay = ref(false)
const isRegisterDisplay = ref(false)

const displayReg = () => {
  isLoginDisplay.value = false
  isRegisterDisplay.value = !isRegisterDisplay.value

};
</script>