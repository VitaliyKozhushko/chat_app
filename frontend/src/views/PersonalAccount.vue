<template>
  <div class="personal-account-page">
    <div class="messenger">
      <Menu/>
      <ListItems/>
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
import {computed, onMounted} from 'vue'
import {useStore} from 'vuex'
import { io } from 'socket.io-client'

const store = useStore()

let socket = null

const actualItemMenu = computed(() => store.state.actualItemMenu)

const displayDialog = computed(() => {
  return ['chats', 'rooms'].includes(actualItemMenu.value)
})

onMounted(() => {
  const access_token = localStorage.getItem('access_token');
  socket = io("http://localhost:8000/", {
    query: {
      auth_token: access_token
    },
    transports: ["websocket"]
  });

  socket.on("connect", () => {
    console.log("Connected to WebSocket server!");
  });

  socket.on("disconnect", () => {
    console.log("Disconnected from WebSocket server");
  });
})
</script>