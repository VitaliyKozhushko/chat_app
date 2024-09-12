<template>
  <el-dialog
      :model-value="displayModal"
      title="Название комнаты"
      width="500"
      @close="closeDialog"
  >
    <template #default>
      <div v-if="loading" class="loading-overlay is-loading">
        <el-icon class="is-loading">
          <Loading/>
        </el-icon>
      </div>
      <el-input v-model="name" :disabled="loading" placeholder="Название комнаты"/>
    </template>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="closeDialog">Отмена</el-button>
        <el-button type="primary" @click="createRoom">
          Создать
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import {ref, defineProps, defineEmits} from 'vue';
import axios from '@/axios.js';
import {ElNotification} from 'element-plus';

const props = defineProps({
  displayModal: {
    type: Boolean,
    required: true
  }
});

const emit = defineEmits(['update:displayModal', 'update-rooms']);

const name = ref('');
const loading = ref(false);

const closeDialog = () => {
  emit('update:displayModal', false);
};

async function createRoom() {
  try {
    loading.value = true;
    const accessToken = localStorage.getItem('access_token');
    let data = new FormData();
    data.set('name', name.value);
    const response = await axios.post('/rooms', data, {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
      }
    });
    emit('update-rooms', response.data);
  } catch (err) {
    let errMes = err.response?.data?.detail || 'Невозможно создать комнату. Попробуйте позже';
    ElNotification({
      title: 'Ошибка',
      message: errMes,
      type: 'error',
      position: 'bottom-right'
    });
  } finally {
    loading.value = false;
    closeDialog();
  }
}
</script>

<style scoped>
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  pointer-events: none;
}
</style>
