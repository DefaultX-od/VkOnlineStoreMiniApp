<script setup>
import { computed } from 'vue';

import noImg from '@/assets/icons/no-img.png' 

const props = defineProps({
    imgSource: String
})

const validSrc = computed (() => props.imgSource && props.imgSource !=='null' ? props.imgSource : noImg)
</script>

<template>
    <div class="gallery-item">
        <img referrerpolicy="no-referrer" :src="validSrc">
    </div>
</template>

<style scoped>
.gallery-item {
    background-color: var(--color-bg-secondary);
    min-width: 100%;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}
.gallery-item img {
    height: 100%;
    width: 100%;
    aspect-ratio: 1/1;
    object-fit: contain;
}
</style>