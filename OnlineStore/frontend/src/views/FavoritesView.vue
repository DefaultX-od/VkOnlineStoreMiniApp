<script setup>
import { ref } from 'vue'
import { getAuthToken } from '@/utils/misc'
import ProductsGrid from '@/components/ProductsGrid.vue'

var loading = ref(true)
var groups = ref([])
var showLoadingScreen = ref(false)

fetch('/api/favorites',{
headers:{
    'Authorization': `Bearer ${getAuthToken()}`,
    'Content-Type': 'application/json'
}
})
.then(response =>{
    if (!response.ok) {
        if (response.status === 401){
            throw new Error('Unauthorized access')
        }
        throw new Error('Server error')
    }
    return response.json()
})
.then(data => {
    groups.value = data
})
.catch(error => {
    console.error('Fetch favorites failed:', error)
})
.finally(() => {
    loading.value = false
})

setTimeout(()=>{ showLoadingScreen.value = true }, 300)
</script>

<template>
<Loading v-if="loading && showLoadingScreen"/>
  <div v-if="!loading" class="product-group fade-in">
    <ProductsGrid :groups="groups" :expandable="false"/>
  </div>
</template>

<style>
.product-group{
  width: 95%;
  margin: auto;
}
</style>