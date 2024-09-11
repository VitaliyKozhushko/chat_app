<template>
  <div class="chats-list">
    <el-scrollbar>
      <el-card shadow="hover">
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
  </div>
</template>


<script setup>
import '@/assets/scss/listItems.scss'
</script>