<template>
  <div v-loading="loading" class="chats-list">
    <el-scrollbar>
      <el-card
          v-for="user in usersList"
          :key="user.id"
          :class="{'online' : user.isOnline}"
          shadow="hover"
          @click="displayChat(user)">
        <div v-if="notReadPrivateMes[user.id]" class="notify-count">
          <span>
          {{ notReadPrivateMes[user.id] }}
        </span>
        </div>
        <div class="user-icon">
          <el-icon>
            <User/>
          </el-icon>
        </div>
        <p>
          {{ user.username }}
        </p>
      </el-card>
    </el-scrollbar>
  </div>
</template>


<script setup>
import '@/assets/scss/listItems.scss'
import {onMounted, ref, watch, computed} from "vue"
import axios from "@/axios.js"
import {ElNotification} from "element-plus"
import {useStore} from 'vuex'

const store = useStore()

const loading = ref(false)
const userId = ref(false)
const usersList = ref([])
const actualItemMenu = computed(() => store.state.actualItemMenu)
const notReadPrivateMes = computed(() => store.state.notReadPrivateMes)

watch(actualItemMenu, (newActualItem) => {
  if (newActualItem === 'chats') {
    getUsers()
  }
})

async function getUsers() {
  try {
    loading.value = true
    const [usersResponse, onlineUsersResponse] = await Promise.all([
      axios.get('/users'),
      axios.get('/online-users')
    ]);
    const users = usersResponse.data;
    const onlineUsers = onlineUsersResponse.data;

    let filterUsers = users.filter(user => user.id !== +userId.value)
    filterUsers.forEach(user => {
      user.isOnline = !!onlineUsers.includes(String(user.id))
    })
    usersList.value = filterUsers
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

const displayChat = async (user) => {
  const accessToken = localStorage.getItem('access_token');
  const senderId = localStorage.getItem('userId');
  try {
    const response = await axios.get(`/private_messages/${senderId}-${user.id}`, {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
      }
    })
    const transform_mes = response.data.sort((a, b) => b.id - a.id);
    store.commit('SET_MESSAGES', {type: 'privateMessages', messages: transform_mes});
  } catch (err) {
    let errMes = err.response?.data?.detail || 'Невозможно получить список сообщений для комнаты.Попробуйте позже'
    ElNotification({
      title: 'Ошибка',
      message: errMes,
      type: 'error',
      position: 'bottom-right'
    })
  } finally {
    store.commit('SET_ACTIVE_CHAT', user.id)
    store.commit('REMOVE_NOT_READ_PRIVATE_MES', user.id)
  }
}

onMounted(() => {
  userId.value = localStorage.getItem('userId')
  getUsers()
})
</script>