<script setup>
import { ref } from 'vue';
import CategoriesGrid from '@/components/CategoriesGrid.vue'
import Loading from '@/components/LoadingScreenGrid.vue'

const groups = ref([]); 
const loading = ref(true);
const showLoadingScreen = ref(false);

setTimeout(()=>{
    showLoadingScreen.value = true
}, 300)

fetch('/api/categories')
.then(response =>{
    if(!response){
        throw new Error('Network response was not ok')
    }
    return response.json();
})
.then(data =>{
    groups.value = data
})
.catch(error =>{
    console.error('There was a problem with the fetch operation:', error);
})
.finally(() =>{
    loading.value = false
})
</script>

<template>
    <Loading v-if="loading && showLoadingScreen" :sectionCount="2" :itemsPerSection="4" :isProductGrid="false"/>
        <div v-if="!loading" class="catalog fade-in">
            <CategoriesGrid :groups="groups" />
        </div>
</template>

<style scoped>
.catalog{
  width: 95%;
  margin: auto;
}
</style>