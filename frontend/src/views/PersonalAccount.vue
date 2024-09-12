<template>
  <div class="personal-account-page">
    <div class="messenger">
      <Menu/>
      <ListItems v-if="actualItemMenu !== 'notify'"/>
      <Dialogs v-if="displayDialog"/>
      <div v-else class="logo-block">
        <img class="logo" :src="logo" alt="logo">
        <p>Chat app - общайся легко &#128521;</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import '@/assets/scss/personalAccounts.scss'
import Menu from "@/components/Menu.vue"
import ListItems from '@/components/ListItems/ListItems.vue'
import Dialogs from "@/components/Dialogs.vue"
import logo from "@/assets/logo/logo.png"
import {computed, onMounted,} from 'vue'
import {useStore} from 'vuex'

const store = useStore()

const actualItemMenu = computed(() => store.state.actualItemMenu)
const userId = localStorage.getItem('userId');

const displayDialog = computed(() => {
  return ['chats', 'rooms'].includes(actualItemMenu.value)
})

onMounted(() => {
  const access_token = localStorage.getItem('access_token');
  store.dispatch('initSocket', {access_token, transport: 'websocket', userId});
})
</script>