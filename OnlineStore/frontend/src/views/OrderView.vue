<script setup>
import { onMounted, ref } from 'vue'

import Cart from '@/components/Cart.vue'
import Loading from '@/components/LoadingSpinner.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import OrderStatusSection from '@/components/OrderStatusSection.vue'

import { useOrderFetch } from '@/composables/fetchOrder'
import { getAuthToken } from '@/utils/misc'
import OrderDetailsSection from '@/components/OrderDetailsSection.vue'

const props = defineProps({
    id: Number
})

var showConfirm = ref(false)
var confirmText = ref("")
var pendingAction = ref(null)
var showLoadingScreen = ref(false)

const { loading, orderData, statusesData } = useOrderFetch(props.id)

function confirmCancelOrder(){
    confirmText.value="Вы уверены, что хотите отменить заказ?"
    pendingAction.value = cancelOrder
    showConfirm.value = true
}

function handleConfirm(confirmed){
    showConfirm.value = false;
    if(confirmed && pendingAction.value){
    pendingAction.value();
    pendingAction.value = null;
    }
}

function cancelOrder(){
  fetch(`/api/order/cancel?order_id=${props.id}`,{
    headers: {
      'Authorization': `Bearer ${getAuthToken()}`,
      'Content-Type': 'application/json'
    }
  })
  .then(response =>{
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      return response.json();
  })
  .then(data => {
      orderData.value.is_canceled = data.is_canceled
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
    <div v-if="!orderData.is_canceled" @click="confirmCancelOrder" class="btn-colored full-length">
      <div class="label">Отменить заказ</div>
    </div>
  </div>
  
  <ConfirmDialog 
    :visible="showConfirm"
    :text="confirmText"
    @confirm="handleConfirm"
  />
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