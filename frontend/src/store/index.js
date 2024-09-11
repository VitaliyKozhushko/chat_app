import { createStore } from 'vuex'
import io from 'socket.io-client'

export default createStore({
  state: {
    actualItemMenu: 'chats',
    socket: null,
    activeChat: null,
    messages: []
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
    SET_MESSAGES(state, messages) {
      state.messages = messages
    },
    UPDATE_MESSAGES(state, message) {
      state.messages.unshift(message)
    }
  },
  actions: {
    initSocket({ commit }, {access_token, transport}) {
      const socket = io("http://localhost:8000/", {
      query: {
        auth_token: access_token
      },
      transports: [transport]
      });
      commit('SET_SOCKET', socket);
    }
  },
  getters: {
    getSocket: (state) => state.socket,
  }
})
