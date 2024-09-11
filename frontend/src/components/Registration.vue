<template>
  <div class="signup-block" v-loading="loading">
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
import axios from "@/axios.js";
import {ElNotification} from "element-plus";

const username = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')

const emit = defineEmits(['toggleAuth'])

const login = (isLogin) => {
  emit('toggleAuth', {isLoginDisplay: isLogin, isRegisterDisplay: false})
}

const registration = async () => {
  try {
    loading.value = true
    let data = new FormData()
    data.set('username', username.value)
    data.set('password', password.value)
    const response = await axios.post('/registration', data)
  } catch (err) {
    ElNotification({
      title: 'Ошибка',
        message: err.response.data.detail,
        type: 'error',
        position: 'bottom-right'
      })
  } finally {
    loading.value = false
  }
}
</script>