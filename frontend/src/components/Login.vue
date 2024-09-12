<template>
  <div class="login-block" v-loading="loading">
    <el-input v-model="username" placeholder="username">
    </el-input>
    <el-input v-model="password" type="password" show-password placeholder="password"/>
    <el-button type="primary" class="login-btn" @click="login">Войти</el-button>
    <div class="change-decision">
      <el-text class="mx-1" size="small">Еще нет аккаунта?</el-text>
      <el-button type="primary" @click="() => registration(true)" size="small" link>Регистрация</el-button>
    </div>
    <el-button type="primary" @click="() => registration(false)" link size="small">На главную</el-button>
  </div>
</template>

<script setup>
import {ref, defineEmits} from 'vue'
import axios from '@/axios'
import {ElNotification} from 'element-plus'
import {useRouter} from 'vue-router'
import {useStore} from 'vuex'

const store = useStore()

const emit = defineEmits(['toggleAuth']);
const router = useRouter();

const registration = (isReg) => {
  emit('toggleAuth', {isLoginDisplay: false, isRegisterDisplay: isReg})
}

const username = ref('');
const password = ref('');
const loading = ref(false)

const login = async () => {
  try {
    loading.value = true
    let data = new URLSearchParams({
      username: username.value,
      password: password.value,
    }).toString()
    const response = await axios.post('/login', data, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      }
    })
    localStorage.setItem('access_token', response.data.access_token)
    localStorage.setItem('userId', response.data.user_id)
    router.push('/messenger');
  } catch (err) {
    let errMes = err.response?.data?.detail || 'Не получилось авторизоваться.Попробуйте позже'
    ElNotification({
      title: 'Ошибка',
      message: errMes,
      type: 'error',
      position: 'bottom-right'
    })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.error {
  color: red;
}
</style>
