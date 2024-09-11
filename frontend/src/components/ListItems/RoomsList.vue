<template>
  <div class="rooms-list">
    <el-button type="primary" class="add-room" :icon="Plus">Создать</el-button>
    <el-scrollbar>
      <el-card shadow="hover">
        <p>
          Mikle
        </p>
      </el-card>
    </el-scrollbar>
  </div>
</template>

<script setup>
import { Plus } from '@element-plus/icons-vue'
</script>