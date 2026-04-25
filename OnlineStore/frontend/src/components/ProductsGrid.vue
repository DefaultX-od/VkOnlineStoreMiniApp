<script setup>
import SectionTitle from './SectionTitle.vue';
import Grid from './Grid.vue';
import GridObject from './GridObject.vue';

const props = defineProps({
    groups: Array,
    expandable:{
        type: Boolean,
        default: false
    },
    category_id:{
      type: Number
    }
})
</script>

<template>
    <div v-for="group in groups" :key="group.id">
      <SectionTitle :title="group.name" :expandable="expandable" :category_id="category_id" :group_id="group.id"/>
      <Grid>
        <GridObject 
        v-for="product in group.products"
        :key="product.id"
        :text="product.name"
        :image="product.img"
        :id="product.id"
        :isProduct="true"
        :normalPrice="product.price"
        :discountPrice="product.discount_price"
        :link="`/catalog/product/${product.id}`"
        />
      </Grid>
    </div>
</template>