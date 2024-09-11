<template>
  <div class="dialogs">
    <div class="dialogs-block" v-if="activeChat">
      <el-scrollbar>
        <el-card
          v-for="mes in messages"
          :key="mes.id"
          class="dialog-card"
          :class="+userId === +mes.sender_id ? 'right' : 'left'"
        >
          <div class="user-icon">
            <el-icon>
              <User />
            </el-icon>
          </div>
          <p class="sender">{{ mes.sender }}</p>
          <p class="message">{{ mes.content }}</p>
        </el-card>
      </el-scrollbar>
      <div class="input-message-block">
        <el-input
          v-model="message"
          ref="messageInput"
          autosize
          type="textarea"
          placeholder="Введите сообщение"
          @keyup.enter="sendMessage"
        />
        <el-button type="primary" class="login-btn" @click="sendMessage">Отправить</el-button>
      </div>
    </div>
    <el-text class="info-text" v-else type="primary" size="large">
      Выберите комнату или пользователя, которому хотите написать сообщение, чтобы начать общение.
    </el-text>
  </div>
</template>

<script setup>
import {useStore} from 'vuex';
import {computed, ref, watch} from 'vue';
import {ElNotification} from 'element-plus';

const store = useStore();
const socket = computed(() => store.getters.getSocket);
const activeChat = computed(() => store.state.activeChat);
const messages = computed(() => store.state.messages);
const userId = localStorage.getItem('userId');
const isSocketListener = ref(false);
const actualItemMenu = computed(() => store.state.actualItemMenu);

const message = ref('');
const messageInput = ref(null);

function sendMesToUser() {
  if (socket.value && message.value.trim() !== '') {
    console.log(activeChat.value)
    console.log(message.value)
    socket.value.emit('private_message', {
      to: activeChat.value,
      from: userId,
      message: message.value,
    });
    message.value = '';
    messageInput.value.blur();
  } else {
    ElNotification({
      title: 'Ошибка',
      message: 'Не получилось отправить приватное сообщение. Попробуйте позже',
      type: 'error',
      position: 'bottom-right',
    });
  }
}

const sendMessage = () => {
  if (actualItemMenu.value === 'chats') {
    sendMesToUser();
    return;
  }
  if (socket.value && message.value.trim() !== '') {
    socket.value.emit('send_message', {
      content: message.value,
      room_id: activeChat.value,
    });
    message.value = '';
    messageInput.value.blur();
  } else {
    ElNotification({
      title: 'Ошибка',
      message: 'Не получилось отправить сообщение. Попробуйте позже',
      type: 'error',
      position: 'bottom-right',
    });
  }
};

function updMes(data) {
  console.log(data);
  store.commit('UPDATE_MESSAGES', JSON.parse(data));
}

watch(activeChat, (newActiveChat, oldActiveChat) => {
  if (newActiveChat !== oldActiveChat) {
    if (oldActiveChat) {
      socket.value.off('send_message', updMes);
    }
    if (newActiveChat) {
      socket.value.on('send_message', updMes);
    }
    isSocketListener.value = !!newActiveChat;
  }
});
</script>
