<template>
  <div class="rooms-list">
    <el-button type="primary" class="add-room" :icon="Plus">Создать</el-button>
    <div v-loading="loading">
      <el-text type="primary" size="large">Доступные комнаты</el-text>
      <el-scrollbar class="available-rooms">
        <el-card v-for="room in availableRooms" :key="room.id" shadow="hover">
          <p>
            {{ room.name }}
          </p>
          <el-button type="primary" @click="connectRoom(room)" size="small">Подключиться</el-button>
        </el-card>
      </el-scrollbar>
    </div>
    <div>
      <el-text type="primary" size="large">Комнаты пользователя</el-text>
      <el-scrollbar class="user-rooms">
        <el-card v-for="room in userRooms" :key="room.id" shadow="hover">
          <p>
            {{ room.name }}
          </p>
          <el-button type="primary" @click="leaveRoom(room)" size="small">Покинуть</el-button>
        </el-card>
      </el-scrollbar>
    </div>
  </div>
</template>

<script setup>
import {Plus} from '@element-plus/icons-vue'
import axios from "@/axios.js";
import {ElNotification} from "element-plus"
import {ref, onMounted} from 'vue'
import {useStore} from 'vuex'

const store = useStore()

const socket = store.getters.getSocket;

const loading = ref(false)
const availableRooms = ref([])
const userRooms = ref([])
const userId = ref('')

const displayRooms = (rooms) => {
  rooms.forEach(room => {
    let roomsUsers = room.users.length ? room.users : []
    let userInRoom = roomsUsers.length
        ? !!roomsUsers.find(user => user.id === Number(userId.value))
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
    let errMes = err.response?.data?.detail || 'Невозможно получить список комнат.Попробуйте позже'
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

const moveToUserRooms = (roomId) => {
  const roomIndex = availableRooms.value.findIndex(room => room.id === roomId)
  if (roomIndex !== -1) {
    userRooms.value.push(availableRooms.value[roomIndex]);
    availableRooms.value.splice(roomIndex, 1);
  }
}

const moveToAvailableRooms = (roomId) => {
  const roomIndex = userRooms.value.findIndex(room => room.id === roomId)

  if (roomIndex !== -1) {
    availableRooms.value.push(userRooms.value[roomIndex]);
    userRooms.value.splice(roomIndex, 1);
  }
}

const connectRoom = (room) => {
  if (socket) {
    socket.emit('connect_room', {room_id: room.id, user_id: userId.value})

    const result_connection = (data) => {
      if (data.error) {
        ElNotification({
          title: 'Ошибка',
          message: data.error,
          type: 'error',
          position: 'bottom-right'
        })
      } else {
        moveToUserRooms(data.room_id)
        ElNotification({
          title: 'Успех',
          message: `Вы успешно добавлены в комнату ${room.name}`,
          type: 'success',
          position: 'bottom-right'
        })
      }
      socket.off('connect_room_result', result_connection);
    };

    socket.on('connect_room', result_connection);
  }
}

const leaveRoom = (room) => {
  if (socket) {
    socket.emit('disconnect_room', {room_id: room.id, user_id: userId.value})

    const result_disconnection = (data) => {
      if (data.error) {
        ElNotification({
          title: 'Ошибка',
          message: data.error,
          type: 'error',
          position: 'bottom-right'
        })
      } else {
        moveToAvailableRooms(data.room_id)
        ElNotification({
          title: 'Успех',
          message: `Вы успешно покинули комнату ${room.name}`,
          type: 'success',
          position: 'bottom-right'
        })
      }
      socket.off('disconnect_room', result_disconnection);
    };

    socket.on('disconnect_room', result_disconnection);
  }
}

onMounted(() => {
  userId.value = localStorage.getItem('userId')
  loadRooms()
})
</script>