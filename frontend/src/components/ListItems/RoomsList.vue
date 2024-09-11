<template>
  <div class="rooms-list">
    <el-button type="primary" class="add-room" :icon="Plus">Создать</el-button>
    <div v-loading="loading">
      <el-text type="primary" size="large">Доступные комнаты</el-text>
      <el-scrollbar>
        <el-card v-for="room in availableRooms" :key="room.id" shadow="hover">
          <p>
            {{ room.name }}
          </p>
        </el-card>
      </el-scrollbar>
    </div>
    <div>
      <el-text type="primary" size="large">Комнаты пользователя</el-text>
      <el-scrollbar>
        <el-card v-for="room in userRooms" :key="room.id" shadow="hover">
          <p>
            {{ room.name }}
          </p>
        </el-card>
      </el-scrollbar>
    </div>
  </div>
</template>

<script setup>
import { Plus } from '@element-plus/icons-vue'
import axios from "@/axios.js";
import {ElNotification} from "element-plus"
import { ref, onMounted } from 'vue'

const loading = ref(false)
const availableRooms = ref([])
const userRooms = ref([])

const displayRooms = (rooms) => {
  const userId = localStorage.getItem('userId');
  rooms.forEach(room => {
    let roomsUsers = room.users.length ? room.users : []
    let userInRoom = roomsUsers.length
        ? !!roomsUsers.find(user => user.id === Number(userId))
        : false
    userInRoom ? userRooms.value.push(room) : availableRooms.value.push(room)
  });
}

const loadRooms = async () => {
  try {
    loading.value = true
    const response = await axios.get('/rooms')
    displayRooms(response.data)
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

onMounted(() => {
  console.log(54)
  loadRooms()
})
</script>