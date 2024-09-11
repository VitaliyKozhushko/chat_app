// store/index.js
import { createStore } from 'vuex'

export default createStore({
  state: {
    actualItemMenu: 'chats'
  },
  mutations: {
    setActualItemMenu(state, newItem) {
      state.actualItemMenu = newItem;
    }
  }
})
