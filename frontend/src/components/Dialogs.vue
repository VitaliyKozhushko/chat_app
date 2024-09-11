<template>
  <div class="dialogs">
    <el-scrollbar v-if="activeChat">
      <el-card
          v-for="mes in messages"
          :key="mes.id"
          class="dialog-card"
          :class="+userId === mes.sender_id ? 'right' : 'left'">
        <div class="user-icon">
          <el-icon>
            <User />
          </el-icon>
        </div>
        <p class="sender">
          {{mes.sender}}
        </p>
        <p class="message">
          {{mes.content}}
        </p>
      </el-card>
    </el-scrollbar>
    <el-text class="info-text" v-else type="primary" size="large">
      Выберите комнату в которой состоит пользователь или пользователя, которому хотите написать сообщение, чтобы начать общение
    </el-text>
  </div>
</template>

<script setup>
import {useStore} from 'vuex'
import {computed} from "vue";

const store = useStore()

const activeChat = computed(() => store.state.activeChat)
const messages = computed(() => store.state.messages)
const userId = localStorage.getItem('userId')

console.log(messages.value)
</script>