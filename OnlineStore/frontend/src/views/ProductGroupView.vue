<script setup>
import { ref } from 'vue'

import Loading from '@/components/LoadingScreenGrid.vue'
import ProductsGrid from '@/components/ProductsGrid.vue'

var loading = ref(true)
var groups = ref([])
var showLoadingScreen = ref(false)

const props = defineProps({
    group_id: Number,
    category_id: Number
})

fetch(`/api/group?group_id=${props.group_id}&category_id=${props.category_id}`)
.then(response =>{
    if (!response.ok) {
        if (response.status === 404) {
            throw new Error('Not found')
        }
        throw new Error('Server error')
    }
    return response.json()
})
.then(data => {
    groups.value = data
})
.catch(error => {
    console.error('Fetch group failed:', error)
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

<style scoped>
.product-group{
  width: 95%;
  margin: auto;
}
</style>