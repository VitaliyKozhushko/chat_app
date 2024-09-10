<template>
  <main>
    <Auth v-if="!isEnter" @toggleEnter="isEnter = !isEnter"/>
    <PersonalAccount v-if="isEnter"/>
  </main>
</template>

<script setup>
import Auth from '@/views/Auth.vue'
import PersonalAccount from "@/views/PersonalAccount.vue"
import {ref} from 'vue'

const isEnter = ref(true)

</script>