<script setup>
import SectionTitle from './SectionTitle.vue';
import Grid from './Grid.vue';
import GridObject from './GridObject.vue';

const props = defineProps({
    sectionCount:{
        type: Number,
        default: 3
    },
    itemsPerSection:{
        type: Number,
        default: 2
    },
    isProductGrid:{
        type: Boolean,
        default: true
    }
})
</script>

<template>
    <div v-for="i in sectionCount" class="loading">
        <SectionTitle :blank="true"/>
        <Grid>
            <GridObject v-for="j in itemsPerSection" :blank="true" :isProduct="isProductGrid" :link="''"></GridObject>
        </Grid>
    </div>
</template>

<style scoped>
.loading{
    width: 95%;
    margin: auto;
}
</style>