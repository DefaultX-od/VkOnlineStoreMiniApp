<template>
    <div class="grid-container">
        <slot />
    </div>
</template>

<style scoped>
.grid-container{
    margin: 0 auto;
    display: grid;
    grid-template-columns: 
        calc(50% - var(--gap)/2) 
        calc(50% - var(--gap)/2);
    gap: var(--gap);
    --gap: 8px;
}
</style>