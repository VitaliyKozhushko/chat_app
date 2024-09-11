<template>
  <div class="notify-list">
    <el-scrollbar>
      <el-card shadow="hover" @click="() => directToInfo('rooms')">
        <el-icon>
          <Close />
        </el-icon>
        <p>
          Mikle
        </p>
      </el-card>
    </el-scrollbar>
  </div>
</template>

<script setup>
import {useStore} from 'vuex'

const store = useStore()

const directToInfo = (direction) => {
  store.commit('setActualItemMenu', direction)
}
</script>