<script setup>
import { ref } from 'vue';

import Loading from '@/components/LoadingScreenGrid.vue';
import ProductsGrid from '@/components/ProductsGrid.vue';

var loading = ref(true)
var groups = ref([])
var showLoadingScreen = ref(false)

const props = defineProps({
    id: Number
})
fetch(`/api/category?category_id=${props.id}`)
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

setTimeout(()=>{ showLoadingScreen.value = true }, 300)
</script>

<template>
  <Loading v-if="loading && showLoadingScreen"/>
  <div v-if="!loading" class="category fade-in">
    <ProductsGrid :groups="groups" :expandable="true"  :category_id="id"/>
  </div>
</template>

<style scoped>
.category{
  width: 95%;
  margin: auto;
}
</style>