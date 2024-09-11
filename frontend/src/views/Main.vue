<template>
  <main>
    <Auth v-if="!isEnter"/>
    <PersonalAccount v-else/>
  </main>
</template>

<script setup>
import Auth from '@/views/Auth.vue'
import PersonalAccount from "@/views/PersonalAccount.vue"
import {ref} from 'vue'

const isEnter = ref(false)

</script>