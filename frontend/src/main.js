import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { io } from 'socket.io-client'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const socket = io('http://localhost:8000')

const app = createApp(App)
app.config.globalProperties.$socket = socket

app.use(router)
app.use(ElementPlus)

app.mount('#app')
