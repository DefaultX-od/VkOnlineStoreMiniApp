<script setup>
import { onMounted, ref } from 'vue';
import OrderCard from '@/components/OrderCard.vue';
import { getAuthToken } from '@/utils/misc';

var orders = ref([])
var loading = ref(true)

function fetchOrders(){
    fetch('/api/orders',{
            headers: {
                'Authorization': `Bearer ${getAuthToken()}`,
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok')
            }
            return response.json()
        })
        .then(data => {
            orders.value = data
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error)
        })
        .finally(() =>{
            loading.value = false
        })
}

onMounted(() =>{
    fetchOrders()
})

</script>

<template>
<div class="list-container">
    <OrderCard v-for="order in orders"
    :orderId="order.id"
    :orderStatus="order.status"
    :productsQuantity="order.cart.items_count"
    :products="order.cart.items"
    :date="order.date"
    :isCanceled="order.is_canceled"
    :isCompleted="order.is_completed"
    />
</div>
</template>

<style scoped>
.list-container {
    width: 100%;
    gap: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
}
</style>