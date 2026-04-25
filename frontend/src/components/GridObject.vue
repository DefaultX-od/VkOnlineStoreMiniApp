<script setup>
import { RouterLink } from 'vue-router'
import { computed } from 'vue'
import imagePlaceholder from '@/assets/icons/no-img.png'
import PriceContainer from './PriceContainer.vue'

const props = defineProps({
    id: Number,
    text: String,
    isProduct: Boolean,
    image: String,
    blank: Boolean,
    link: String,
    normalPrice: Number,
    discountPrice: Number,
    iconSymbolic: Boolean
})

const validSrc = computed (() => props.image && props.image !== null ? props.image : imagePlaceholder)
</script>

<template>
    <RouterLink
    :to="link"
    class="grid-object">
    <div v-if="blank" class="grid-object-img-container blank">
        <div class="img-placeholder"></div>
    </div>
    <div v-else class="grid-object-img-container" :class="{symbolic : iconSymbolic}">
        <img referrerpolicy="no-referrer" :src="validSrc" loading="lazy">
    </div>
    <div v-if="blank && isProduct" class="blank-text-small-v1"></div>
    <PriceContainer v-else v-if="isProduct" :discountPrice="discountPrice" :normalPrice="normalPrice"/>
    <div v-if="blank" class="blank-text-small-v2"></div>
    <div v-else :class="{'grid-object-text': !isProduct, 'product-name': isProduct}">{{ text }}</div>
    <div v-if="blank && isProduct" class="blank-text-small-v1"></div>
    </RouterLink>
</template>

<style>
.grid-object {
    position: relative;
    display: inherit;
    gap: 5px;
    border-radius: 25px;
    padding: 8px;
    background-color: var(--color-bg-secondary);
}
.grid-object-img-container{
    background-color: var(--color-bg-secondary);
    border-radius: 25px;
}

.grid-object-img-container.symbolic{
    padding: 30px;
}

.grid-object-img-container img{
    width: 100%;
    border-radius: 15px;
    aspect-ratio: 1/1;
    object-fit: contain;
}

.product-name{
    font-size: 14px;
    font-weight: bold;
    overflow: hidden;
    position: relative;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    color: var(--color-text-secondary);
    line-height: 1.1;
}

.grid-object .product-name{
    word-break: break-all;    
    line-clamp: 2;
    -webkit-line-clamp: 2;
    min-height: calc(1.1em * 2);
    max-height: calc(1.1em * 2);
}

.grid-object-text {
    bottom: 0;
    left: 0;
    margin-bottom: 10px;
    margin-left: 10px;
    margin-right: 10px;
    font-size: 14px;
    color: var(--color-text-secondary);
    font-weight: bold;
    position: absolute;
    word-break: break-word;
}
</style>