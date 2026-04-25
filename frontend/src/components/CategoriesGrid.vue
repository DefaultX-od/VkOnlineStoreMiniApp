<script setup>
import Grid from '@/components/Grid.vue'
import GridObject from '@/components/GridObject.vue'
import SectionTitle from '@/components/SectionTitle.vue'

const props = defineProps({
    groups: Array
})
</script>

<template>
    <div v-for="group in groups" :key="group.id">
      <SectionTitle :title="group.name" />
      <Grid>
        <GridObject 
        v-for="category in group.categories"
        :key="category.id"
        :text="category.name"
        :image="category.icon"
        :id="category.id"
        :blank="false"
        :link="`/catalog/category/${category.id}`"
        />
      </Grid>
    </div>
</template>