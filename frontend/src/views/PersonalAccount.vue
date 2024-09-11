<template>
  <div class="personal-account-page">
    <Menu/>
    <ListItems/>
    <Dialogs v-if="displayDialog"/>
    <div v-else class="logo-block">
      <img class="logo" :src="logo" alt="logo">
      <p>Chat app - общайся легко &#128521;</p>
    </div>
  </div>
</template>

<script setup>
import '@/assets/scss/personalAccounts.scss'
import Menu from "@/components/Menu.vue"
import ListItems from '@/components/ListItems/ListItems.vue'
import Dialogs from "@/components/Dialogs.vue"
import logo from "@/assets/logo/logo.png"
import {computed} from 'vue'
import {useStore} from 'vuex'

const store = useStore()

const actualItemMenu = computed(() => store.state.actualItemMenu)

const displayDialog = computed(() => {
  return ['chats', 'rooms'].includes(actualItemMenu.value)
})
</script>