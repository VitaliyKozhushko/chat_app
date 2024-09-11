// store/index.js
import { createStore } from 'vuex'

export default createStore({
  state: {
    actualItemMenu: 'chat'
  },
  mutations: {
    setActualItemMenu(state, newItem) {
      state.actualItemMenu = newItem;
    }
  },
  actions: {
    increment({ commit }) {
      commit('increment')
    },
    decrement({ commit }) {
      commit('decrement')
    }
  },
  getters: {
    doubleCount: (state) => state.count * 2
  }
})
