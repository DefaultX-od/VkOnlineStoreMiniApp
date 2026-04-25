<script setup>
import { getAuthToken } from '@/utils/misc'
import { computed, ref } from 'vue'

import { useOrderFetch } from '@/composables/fetchOrder'

import Cart from '@/components/Cart.vue'
import Loading from '@/components/LoadingSpinner.vue'
import OrderStatusSection from '@/components/OrderStatusSection.vue'
import OrderDetailsSection from '@/components/OrderDetailsSection.vue'

var showLoadingScreen = ref(false)

const props = defineProps({
    id: Number
})

const { loading, orderData, statusesData, refetch } = useOrderFetch(props.id)

const nextStatusInfo = computed(()=>{

  const order = orderData.value
  const statuses = statusesData.value

  if(!order.status_id || !statuses.length) return null

  const currentIndex = statuses.findIndex(s => s.id === order.status_id)
  const isLastStatus = currentIndex === statuses.length - 1;

  if (isLastStatus) {
    return { isFinalStep: true, label: 'Заказ выдан' };
  }

  return {
    isFinalStep: false,
    status: statuses[currentIndex + 1],
    label: `Перевести в статус ${statuses[currentIndex + 1].name}`
  }
})

function updateOrderStatus(){
  fetch('/api/orders/admin/update',{
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${getAuthToken()}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      'order_id': props.id,
      'status_id': nextStatusInfo.value.status?.id,
      'is_completed': nextStatusInfo.value.isFinalStep
    })
  })
  .then(response =>{
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      return response.json();
  })
  .then(data => {
      refetch()
  })
  .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
  })
  .finally(() => {
  })
}

setTimeout(()=>{ showLoadingScreen.value = true }, 300)
</script>

<template>
  <Loading v-if="loading && showLoadingScreen" />
  <div v-if="!loading" class="order fade-in">
    <OrderStatusSection
    :isCanceled="orderData.is_canceled"
    :isCompleted="orderData.is_completed"
    :statuses="statusesData"
    :currentStatusId="orderData.status_id"
     />
    <OrderDetailsSection
    :dropPoint="orderData.drop_point"
    :paymentMethod="orderData.payment_method"
    />
    <Cart 
    :items="orderData.cart.items"
    :itemsCount="orderData.cart.items_count"
    :fullPrice="orderData.cart.full_price"
    :totalDiscount="orderData.cart.total_discount"
    :total="orderData.cart.total"
    :updating="false"
    :readOnly="true"
    />
    <div v-if="orderData && !orderData.is_canceled && !orderData.is_completed" @click="updateOrderStatus" class="btn-colored full-length">
      <div class="label">{{ nextStatusInfo.label }}</div>
    </div>
  </div>
</template>

<style scoped>
.order {
  display: flex;
  position: absolute;
  width: 100%;
  flex-direction: column;
  padding-bottom: 80px;
  gap: 10px;
}
</style>