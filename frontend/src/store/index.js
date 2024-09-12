import { createStore } from 'vuex'
import io from 'socket.io-client'

export default createStore({
  state: {
    actualItemMenu: 'chats',
    socket: null,
    activeChat: null,
    messages: [],
    privateMessages: []
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
    }
  },
  actions: {
    initSocket({ commit }, {access_token, transport, userId}) {
      const socket = io("http://localhost:8000/", {
      query: {
        auth_token: access_token
      },
      transports: [transport]
      });
      socket.emit('register', userId);
      socket.on('send_message', (data) => {
        console.log(data)
        commit('UPDATE_MESSAGES', {type: 'message', message: JSON.parse(data)})
      });
      socket.on('private_message', (data) => {
        console.log(data)
        commit('UPDATE_MESSAGES', {type: 'privateMessages', message: data})
      });
      commit('SET_SOCKET', socket);
    }
  },
  getters: {
    getSocket: (state) => state.socket,
  }
})
