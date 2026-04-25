import './assets/base.css'
import './assets/colors.css'
import './assets/icons.css'
import './assets/text.css'
import './assets/widgets.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const tg = window.Telegram?.WebApp
if (tg) {
  router.afterEach((to, from) => {
    if (to.path !== '/') {
      tg.BackButton.show()
    } else {
      tg.BackButton.hide()
    }
  })

  tg.BackButton.onClick(() => {
    window.history.back()
  })
}

const app = createApp(App)

app.use(router)

app.mount('#app')
