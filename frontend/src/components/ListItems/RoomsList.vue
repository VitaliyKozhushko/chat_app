<template>
  <div class="rooms-list">
    <el-button type="primary" class="add-room" :icon="Plus">Создать</el-button>
    <div>
      <el-text type="primary" size="large">Доступные комнаты</el-text>
      <el-scrollbar>
        <el-card shadow="hover">
          <p>
            Mikle
          </p>
        </el-card>
      </el-scrollbar>
    </div>
    <div>
      <el-text type="primary" size="large">Комнаты пользователя</el-text>
      <el-scrollbar>
        <el-card shadow="hover">
          <p>
            Mikle
          </p>
        </el-card>
      </el-scrollbar>
    </div>
  </div>
</template>

<script setup>
import { Plus } from '@element-plus/icons-vue'
</script>