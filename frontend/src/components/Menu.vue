<template>
  <div class="menu">
    <div class="logo-mini">
      <img :src="logo_mini" alt="logo_mini"/>
      <img class="exit-icon" :src="exit_icon" alt="exit" @click="handleLogout"/>
    </div>
    <div class="menu-items">
      <el-icon
          size="24"
          :class="{'active': actualItemMenu === 'chats', 'hasMes': hasNotReadPrivateMes}"
          @click="() => changeMenuItem('chats')">
        <User/>
      </el-icon>
      <el-icon size="24" :class="{'active': actualItemMenu === 'rooms'}" @click="() => changeMenuItem('rooms')">
        <Files/>
      </el-icon>
      <el-icon size="24" :class="{'active': actualItemMenu === 'notify'}" @click="() => changeMenuItem('notify')">
        <Bell/>
      </el-icon>
    </div>
  </div>
</template>

<script setup>
import '@/assets/scss/menu.scss'
import logo_mini from '@/assets/logo/logo_small.png'
import exit_icon from '@/assets/icons/logout.png'
import {computed} from 'vue'
import {useStore} from 'vuex'
import {logout} from '@/router/auth.js'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter();

const actualItemMenu = computed(() => store.state.actualItemMenu)
const socket = computed(() => store.getters.getSocket)
const hasNotReadPrivateMes = computed(() => store.state.hasNotReadPrivateMes)

const changeMenuItem = (newItem) => {
  store.commit('SET_ACTUAL_ITEM_MENU', newItem)
  store.commit('SET_ACTIVE_CHAT', null)
  if (newItem === 'chats' && hasNotReadPrivateMes.value) store.commit('SET_HAS_NOT_READ_PRIVATE_MES')
}

const handleLogout = () => {
  logout()
  socket.value.disconnect()
  router.push('/')
}
</script>
