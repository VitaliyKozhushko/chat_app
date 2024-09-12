import { createStore } from 'vuex'
import io from 'socket.io-client'
import {ElNotification} from 'element-plus';

export default createStore({
  state: {
    actualItemMenu: 'chats',
    socket: null,
    activeChat: null,
    messages: [],
    privateMessages: [],
    notReadPrivateMes: {},
    hasNotReadPrivateMes: false
  },
  mutations: {
    SET_ACTUAL_ITEM_MENU(state, newItem) {
      state.actualItemMenu = newItem;
    },
    SET_SOCKET(state, connection) {
      state.socket = connection
    },
    SET_ACTIVE_CHAT(state, chatId) {
      state.activeChat = chatId
    },
    SET_MESSAGES(state, data) {
      if (data.type === 'message') {
       state.messages = data.messages
      } else {
        state.privateMessages = data.messages
      }
    },
    UPDATE_MESSAGES(state, data) {
      if (data.type === 'message') {
       state.messages.unshift(data.message)
      } else {
        state.privateMessages.unshift(data.message)
      }
    },
    SET_NOT_READ_PRIVATE_MES(state, userId) {
      if (!state.notReadPrivateMes[userId]) {
        state.notReadPrivateMes[userId] = 1
      } else {
       state.notReadPrivateMes[userId] = state.notReadPrivateMes[userId] + 1
      }
    },
    REMOVE_NOT_READ_PRIVATE_MES(state, userId) {
      delete state.notReadPrivateMes[userId]
    },
    SET_HAS_NOT_READ_PRIVATE_MES(state) {
      state.hasNotReadPrivateMes = !state.hasNotReadPrivateMes
    }
  },
  actions: {
    initSocket({ commit, state }, {access_token, transport, userId}) {
      const socket = io("http://localhost:8000/", {
      query: {
        auth_token: access_token
      },
      transports: [transport]
      });
      socket.emit('register', userId);
      socket.on('send_message', (data) => {
        commit('UPDATE_MESSAGES', {type: 'message', message: JSON.parse(data)})
      });
      socket.on('private_message', (data) => {
        const userId = localStorage.getItem('userId')
        console.log('userId:', userId)
        console.log('data:', data)
        if (!data.to_sender && (state.actualItemMenu !== 'chats' || state.activeChat !== +data.sender_id)) {
          commit('SET_NOT_READ_PRIVATE_MES', data.sender_id)
          ElNotification({
            message: `Получено новое сообщение от ${data.sender}`,
            type: 'success',
            position: 'top-right',
          });
        }
        if (!data.to_sender && state.actualItemMenu !== 'chats') commit('SET_HAS_NOT_READ_PRIVATE_MES')
      });
      commit('SET_SOCKET', socket);
    }
  },
  getters: {
    getSocket: (state) => state.socket,
  }
})
