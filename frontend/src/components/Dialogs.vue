<template>
  <div class="dialogs">
    <el-scrollbar v-if="activeChat">
      <el-card class="dialog-card left">
        <div class="user-icon">
          <el-icon>
            <User />
          </el-icon>
        </div>
        <p>
          Mikle
        </p>
      </el-card>
      <el-card class="dialog-card right">
        <div class="user-icon">
          <el-icon>
            <User />
          </el-icon>
        </div>
        <p>
          Mikle
        </p>
      </el-card>
    </el-scrollbar>
    <el-text class="info-text" v-else type="primary" size="large">Выберите комнату или пользователя, чтобы начать общение</el-text>
  </div>
</template>

<script setup>
import {useStore} from 'vuex'

const store = useStore()

const activeChat = store.getters.getActiveChat
</script>