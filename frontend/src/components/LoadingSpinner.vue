<script setup>
import spinnerIcon from '@/assets/spinner.gif'
</script>

<template>
    <div class="loading-container" style="display: flex;">
         <img :src="spinnerIcon" class="loading-img">
    </div>
</template>
<style>
.loading-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}
.loading-img {
    width: 56px;
    height: 56px;
}
</style>