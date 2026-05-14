<script setup>
import { onMounted, ref } from 'vue'
import OrderCard from '@/components/OrderCard.vue'
import { getAuthToken } from '@/utils/misc'

var orders = ref([])
var loading = ref(true)

const props = defineProps({
    status_id: Number,
    is_canceled: Boolean,
    is_completed: Boolean
})

function fetchOrdersAdmin(){
    fetch(`/api/admin/orders?status_id=${props.status_id}&is_canceled=${props.is_canceled}&is_completed=${props.is_completed}`,{
            headers: {
                'Authorization': `Bearer ${getAuthToken()}`,
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                if (response.status === 400) {
                    throw new Error('Bad Request')
                }
                else if (response.status === 401) {
                    throw new Error('Unauthorized access')
                }
                else if (response.status === 403) {
                    throw new Error('Forbidden')
                }
                throw new Error('Server error')
            }
            return response.json();
        })
        .then(data => {
            orders.value = data
        })
        .catch(error => {
            console.error('Fetch orders failed:', error)
        })
        .finally(() =>{
            loading.value = false
        })
}

onMounted(() =>{
    fetchOrdersAdmin()
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