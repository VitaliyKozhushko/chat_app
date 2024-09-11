<template>
  <div v-loading="loading" class="chats-list">
    <el-scrollbar>
      <el-card
          v-for="user in usersList"
          :key="user.id"
          :class="{'online' : user.isOnline}"
          shadow="hover"
          @click="displayChat(user)">
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
import {onMounted, ref, watch, computed} from "vue"
import axios from "@/axios.js"
import {ElNotification} from "element-plus"
import {useStore} from 'vuex'

const store = useStore()

const loading = ref(false)
const userId = ref(false)
const usersList = ref([])
const actualItemMenu = computed(() => store.state.actualItemMenu)

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

    console.log('Users:', users);
    console.log('Online Users:', onlineUsers);
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

const displayChat = (user) => {
    store.commit('SET_ACTIVE_CHAT', user.id)
  }

onMounted(() => {
  userId.value = localStorage.getItem('userId')
  getUsers()
})
</script>