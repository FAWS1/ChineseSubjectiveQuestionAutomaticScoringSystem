import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// 🔥 引入 Element Plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// ✅ 可选：Element Plus 图标支持
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ElementPlus)

// 🔧 注册所有 Element Plus 图标为全局组件
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(`i-ep-${key}`, component)
}

app.mount('#app')
