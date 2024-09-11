<template>
  <div v-loading="loading" class="chats-list">
    <el-scrollbar>
      <el-card v-for="user in usersList" :key="user.id" shadow="hover" @click="displayChat(user)">
        <div class="user-icon">
          <el-icon>
            <User />
          </el-icon>
        </div>
        <p>
          {{user.username}}
        </p>
      </el-card>
    </el-scrollbar>
  </div>
</template>


<script setup>
import '@/assets/scss/listItems.scss'
import {onMounted, ref} from "vue"
import axios from "@/axios.js"
import {ElNotification} from "element-plus"
import {useStore} from 'vuex'

const store = useStore()

const loading = ref(false)
const userId = ref(false)
const usersList = ref([])

async function getUsers() {
  try {
    loading.value = true
    const response = await axios.get('/users')
    usersList.value = response.data.filter(user => user.id !== +userId.value)
  } catch (err) {
    let errMes = err.response?.data?.detail || 'Невозможно получить список пользователей.Попробуйте позже'
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

const displayChat = (user) => {
    store.commit('SET_ACTIVE_CHAT', true)
  }

onMounted(() => {
  userId.value = localStorage.getItem('userId')
  getUsers()
})
</script>