<script setup>
import expandIcon from '@/assets/icons/right-arrow.png'
import { RouterLink } from 'vue-router';

const props = defineProps({
    title:{
        type: String,
        required: true
    },
    expandable:{
        type: Boolean,
        default: false
    },
    blank:{
        type: Boolean,
        default: false
    },
    category_id: Number
    ,
    group_id: Number
})
</script>

<template>
    <RouterLink v-if="expandable" class="section-container" :to="`/catalog/category/${category_id}/group/${group_id}`">
        <div class="text big bold">{{ title }}</div>
        <img class="icon-small" :src="expandIcon">
    </RouterLink>
    <div v-else class="section-container">
        <div v-if="blank" class="blank-text-big"></div>
        <div v-else class="text big bold">{{ title }}</div>        
    </div>
</template>

<style scoped>
.section-container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding-top: 10px;
    padding-bottom: 10px;
}
</style>