<template>
  <div class="auth-page">
    <div class="logo-block">
      <img class="logo" :src="logo" alt="logo">
      <p>Chat app - общайся легко &#128521;</p>
    </div>
    <div v-if="!isLoginDisplay && !isRegisterDisplay" class="sign-btns">
      <el-button type="primary" link @click="isLoginDisplay = !isLoginDisplay">Войти</el-button>
      <el-button type="primary" link @click="isRegisterDisplay = !isRegisterDisplay">Зарегистрироваться</el-button>
    </div>
    <Login v-if="isLoginDisplay" @toggleAuth="changeSign"/>
    <Registration v-if="isRegisterDisplay" @toggleAuth="changeSign"/>
    <el-button type="primary" link @click="fantomEnter">Лже авторизация</el-button>
  </div>
</template>

<script setup>
import {defineEmits, ref} from 'vue'
import logo from '@/assets/logo/logo.png'
import '@/assets/scss/auth.scss'
import Login from '@/components/Login.vue'
import Registration from '@/components/Registration.vue'


const isLoginDisplay = ref(false)
const isRegisterDisplay = ref(false)

const emit = defineEmits(['toggleEnter'])

const fantomEnter = () => {
  emit('toggleEnter')
}

const changeSign = (data) => {
  isLoginDisplay.value = data.isLoginDisplay
  isRegisterDisplay.value = data.isRegisterDisplay
};
</script>