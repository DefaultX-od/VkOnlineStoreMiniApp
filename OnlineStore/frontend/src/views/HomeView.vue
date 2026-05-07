<script setup>
import { ref } from 'vue'

import CategoriesGrid from '@/components/CategoriesGrid.vue'
import LoadingScreenGrid from '@/components/LoadingScreenGrid.vue'

var showLoadingScreen = ref(false)
var loading = ref(true)
var groups = ref([])

fetch('/api/categories')
.then(response =>{
  if (!response) {
      throw new Error('Server error')
    }
    return response.json()
})
.then(data => {
      groups.value = data;
})
.catch(error => {
      console.error('Failed to fetch categories:', error)
})
.finally(() => {
      loading.value = false
})

setTimeout(()=>{
  showLoadingScreen.value = true
}, 300)
</script>

<template>
  <LoadingScreenGrid v-if="loading && showLoadingScreen" :sectionCount="2" :itemsPerSection="4" :isProductGrid="false"/>
  <div v-if="!loading" class="home fade-in">
    <CategoriesGrid :groups="groups"/>
  </div>
</template>

<style scoped>
.home{
  width: 95%;
  margin: auto;
}
</style>
