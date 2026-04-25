<script setup>
import { ref } from 'vue';

import CategoriesGrid from '@/components/CategoriesGrid.vue'
import LoadingScreenGrid from '@/components/LoadingScreenGrid.vue'

var showLoadingScreen = ref(false)
var loading = ref(true)
var groups = ref([])

fetch('/api/categories')
.then(response =>{
  if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
})
.then(data => {
      groups.value = data;
})
.catch(error => {
      console.error('There was a problem with the fetch operation:', error);
})
.finally(() => {
      loading.value = false;
})

setTimeout(()=>{
  showLoadingScreen.value = true;
}, 300)
</script>

<template>
  <Loading v-if="loading && showLoadingScreen" :sectionCount="2" :itemsPerSection="4" :isProductGrid="false"/>
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
