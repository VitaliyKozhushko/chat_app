<template>
  <div class="signup-block">
    <el-input v-model="username" placeholder="username"/>
    <el-input v-model="password" type="password" show-password placeholder="password"/>
    <el-button type="primary" class="login-btn" @click="registration">Зарегистрироваться</el-button>
    <div class="change-decision">
      <el-text class="mx-1" size="small">Уже есть аккаунт</el-text>
      <el-button type="primary" @click="() => login(true)" link size="small">Войти</el-button>
    </div>
    <el-button type="primary" @click="() => login(false)" link size="small">На главную</el-button>
  </div>
</template>

<script setup>
import {defineEmits, ref} from 'vue'

const username = ref('')
const password = ref('')

const emit = defineEmits(['toggleAuth'])

const login = (isLogin) => {
  emit('toggleAuth', {isLoginDisplay: isLogin, isRegisterDisplay: false})
}

const registration = () => {
  console.log('hello')
}
</script>