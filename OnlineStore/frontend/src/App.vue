<script setup>
import bridge from '@vkontakte/vk-bridge';
import { onMounted, ref } from 'vue';
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import { appWarehouse } from './store';

import AppFooter from './components/AppFooter.vue'
import Loading from './components/LoadingScreenGrid.vue';
import { getInitData } from './utils/misc';
import { admintRoutes } from './router/adminRoutes';
import { userRoutes } from './router/userRoutes';

var isAdmin = ref(false)
var isAuthProcCompleted = ref(false)

const route = useRoute();
const router = useRouter();


onMounted(() => {
  bridge.send("VKWebAppInit")
  authenticate()
})

function authenticate(){
  const urlParams = new URLSearchParams(window.location.search);
  const vkParams = Object.fromEntries(urlParams.entries());

  if(urlParams.has('vk_app_id')){
    const currentPath = window.location.pathname + window.location.search + window.location.hash
    const userId = vkParams.vk_user_id

    fetch('/auth', {
        method: 'POST',
        body: JSON.stringify({
            user_id: userId
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.status === 422) {
            return response.json().then(err => {
                throw new Error(`Validation error: ${JSON.stringify(err)}`);
            });
        }
        return response.json();
    })
    .then(data => {
        document.cookie = `access_token=${data.accessToken}; Secure; SameSite=Strict; Path=/; Max-Age=604800`;
        isAdmin.value=data.isAdmin

        const newRoutes = data.isAdmin ? admintRoutes : userRoutes
    
        newRoutes.forEach(route => {
          router.addRoute(route)
        })
        
        isAuthProcCompleted.value = true

        router.isReady().then(()=>{
          if (currentPath && currentPath !== '/'){
          router.push(currentPath).catch(()=>{
            router.replace('/')
          })
          }
          else{
            router.replace('/')
          }
        })        

        setTimeout(() => getInitData(), 100)

    })
    .catch(error => {
        console.error('Auth error:', error);
    });
  }
}


</script>

<template>
  <Loading v-if="!isAuthProcCompleted" />
  <div v-else id="app">
    <RouterView />
    <AppFooter v-if="!isAdmin && !route.meta.hideFooter"/>
  </div>
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}



@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

}
</style>
