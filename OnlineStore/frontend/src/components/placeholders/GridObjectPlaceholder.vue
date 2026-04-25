<script setup>
const props = defineProps({
    isProduct: Boolean
})
</script>

<template>
    <div class="grid-object-img-container blank">
        <div class="img-placeholder"></div>
    </div>
    <div v-if="isProduct" class="blank-text-snall-v1"></div>
    <div class="blank-text-small-v2"></div>
    <div v-if="isProduct" class="blank-text-small-v1"></div>
</template>