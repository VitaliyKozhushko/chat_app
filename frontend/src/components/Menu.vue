<template>
  <div class="menu">
    <div class="logo-mini">
      <img :src="logo_mini" alt="logo_mini"/>
    </div>
    <div class="menu-items">
      <el-icon size="24" :class="{'active': actualItemMenu === 'chats'}" @click="() => changeMenuItem('chats')">
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
import {computed} from 'vue'
import {useStore} from 'vuex'

const store = useStore()

const actualItemMenu = computed(() => store.state.actualItemMenu)

const changeMenuItem = (newItem) => {
  store.commit('SET_ACTUAL_ITEM_MENU', newItem)
  store.commit('SET_ACTIVE_CHAT', null)
}
</script>
