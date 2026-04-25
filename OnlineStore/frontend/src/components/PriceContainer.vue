<script setup>
const props = defineProps({
    normalPrice: Number,
    discountPrice: Number,
    isProductPage:{
        type: Boolean,
        default: false
    }
})
</script>

<template>
<div v-if="normalPrice === discountPrice" class="product-price" :class="{'big' : isProductPage}">
        {{ normalPrice }} ₽
</div>
    <div v-else>
        <div class="price-container">
            <div class="product-price new" :class="{'big' : isProductPage}" >{{ discountPrice }} ₽</div>
            <div class="product-price old" :class="{'big' : isProductPage}">{{ normalPrice }}</div>
        </div>
    </div>
</template>

<style scoped>
.price-container {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 5px;
}

.product-price{
    font-size: 16px;
    font-weight: bolder;
    color: var(--color-text-primary);
}

.product-price.big{
    font-size: 24px;
}

.product-price.old {
    text-decoration: line-through;
    font-weight: bold;
    color: var(--color-text-quaternary);
    font-size: 8px;
}

.product-price.new {
    color: var(--color-green);
    font-size: 16px;
    font-weight: bolder;
}

.product-price.old.big {
    font-size: 14px;
}

.product-price.new.big {
    font-size: 24px;
}
</style>