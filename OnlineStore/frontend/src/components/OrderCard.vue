<script setup>
import { getProductWordAccordingToQuantity } from '@/utils/misc';
import { computed, ref } from 'vue';

import imagePlaceholder from '@/assets/icons/no-img.png'
import { orderStateLables } from '@/store';

const props = defineProps({
    orderStatus: String,
    orderId: Number,
    productsQuantity: Number,
    products: Array,
    date: String,
    isCanceled: Boolean,
    isCompleted: Boolean
})

const statusLabel = computed(() =>{
    if (props.isCanceled) return orderStateLables.canceled
    if (props.isCompleted) return orderStateLables.completed
    return props.orderStatus
})

const validSrc = (img) => img ? img : imagePlaceholder;
</script>

<template>
    <RouterLink :to="`/orders/order/${orderId}`" id="order-card" class="list-object row-template">
        <div id="order-upper-details" class="list-object-details column-template">
            <div id="status" class="txt-big">{{ statusLabel }}</div>
            <div id="id">{{ date }}</div>
        </div>
        <div id="products-container" class="list-object-gallery-container">
            <div v-for="item in products" id="product-img-container" class="img-container">
                <img referrerpolicy="no-referrer" :src="validSrc(item.product.img)"/>
            </div>
        </div>
        <div id="product-details-lower">
            <div id="products-quantity">{{ `${productsQuantity} ${getProductWordAccordingToQuantity(productsQuantity)}` }}</div>
        </div>
    </RouterLink>
</template>

<style scoped>
.list-object {
    width: 100%;
    display: flex;
    color: black;
    background-color: #fff;
    border-radius: 15px;
    gap: 15px;
    padding: 5px;
    align-items: center;
    align-items: stretch;
    text-decoration: none;
}
.list-object.row-template{
    flex-direction: column;
}
.list-object-details{
    display: flex;
    flex-direction: column;
    width: 100%;
    justify-content: space-between; 
}
.list-object-details.column-template{
    flex-direction: row;
}
.txt-big{
    font-size: 18px;
    font-weight: bold;
}
.list-object-gallery-container{
    display: flex;
    flex-direction: row;
    overflow-x: auto;
    margin: 5px;
    gap: 7px;
}

.list-object-gallery-container .img-container{    
    border-radius: 9px;
    width: 42px;
    height: 42px;
}

.list-object-gallery-container .img-container img{
    object-fit: contain;
    border-radius: 9px;
    width: inherit;
    height: inherit;
    margin-left: 0;
    vertical-align: middle;
}
</style>