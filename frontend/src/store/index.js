import { createStore } from 'vuex'
import io from 'socket.io-client'

export default createStore({
  state: {
    actualItemMenu: 'chats',
    socket: null,
    message: ''
  },
  mutations: {
    setActualItemMenu(state, newItem) {
      state.actualItemMenu = newItem;
    },
    setSocket(state, connection) {
      state.socket = connection
    },
    SET_MESSAGE(state, message) {
      state.message = message;
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
      commit('setSocket', socket);
    }
  },
  getters: {
    getSocket: (state) => state.socket,
    getMessage: (state) => state.message
  }
})
