<script setup>
import Loading from '@/components/LoadingSpinner.vue'
import Cart from '@/components/Cart.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'

import { getProductWordAccordingToQuantity, getAuthToken, getInitData } from '@/utils/misc'
import { onMounted, ref } from 'vue'

var id = ref(0)
var items = ref([])
var itemsCount = ref(0)
var totalDiscount = ref(0.00)
var fullPrice = ref(0.00)
var total = ref(0.00)
var loading = ref(true)
var updating = ref(false)
var showConfirm = ref(false)
var confirmText = ref("")
var pendingAction = ref(null)
var showLoadingScreen = ref(false)

onMounted(() =>{
    fetchCart()
})

function fetchCart(){
    fetch('/api/cart', {
    headers: {
        'Authorization': `Bearer ${getAuthToken()}`,
        'Content-Type': 'application/json'
    }
    })
    .then(response => {
        if (!response.ok) {
        throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        items.value = data.items;
        itemsCount.value = data.items_count;
        fullPrice.value = data.full_price;
        totalDiscount.value = data.total_discount;
        total.value = data.total;
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    })
    .finally(() => {
        loading.value = false;
    })
}

function syncCartItemCount(productId, newCount) {
    if(newCount===0 && itemsCount.value===1){
    itemsCount.value = 0;
    }
    items.value.forEach(item => {
    if (item.product.id == productId) {
        item.quantity = newCount;
        refreshCartSummary()
    }
    })
}

function refreshCartSummary() {
    updating.value = true;
    fetch('/api/cart/refresh_summary', {
    headers: {
        'Authorization': `Bearer ${getAuthToken()}`,
        'Content-Type': 'application/json'
    }
    })
    .then(response => {
        if (!response.ok) {
        throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        itemsCount.value = data.items_count;
        fullPrice.value = data.full_price;
        totalDiscount.value = data.total_discount;
        total.value = data.total;
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    })
    .finally(()=>{
        updating.value = false;
    })
}

function confirmClearCart(){
    confirmText.value="Вы уверены, что хотите очистить корзину?"
    pendingAction.value = clearCart
    showConfirm.value = true
}

function handleConfirm(confirmed){
    showConfirm.value = false;
    if(confirmed && pendingAction.value){
    pendingAction.value();
    pendingAction.value = null;
    }
}

function clearCart(){
    fetch('/api/cart/clear',{
    headers: {
        'Authorization': `Bearer ${getAuthToken()}`,
        'Content-Type': 'application/json'
    }
    })
    .then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
    })
    .then(data => {
        fetchCart()
        getInitData()
    })
    .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
    })
}

setTimeout(() => { showLoadingScreen.value = true }, 300)
</script>

<template>
  <Loading v-if="loading && showLoadingScreen" />
  <div v-if="!loading && itemsCount > 0" class="cart fade-in">
    <Cart 
      v-bind="{ items, itemsCount, fullPrice, totalDiscount, total, updating }"
      :readOnly="false"
      @syncCount="syncCartItemCount"
      @clear="confirmClearCart"
    />
    <RouterLink :to="'/cart/checkout'" :class=" {'disabled' : updating} ">
        <div class="btn-colored full-length">
            <div class="label">Перейти к оформлению</div>
        </div>
    </RouterLink>
  </div>
  <div v-if="!loading && itemsCount <= 0" class="cart-empty"><div class="text bigger bold" style="text-align: center; opacity: 50%;">Ваша корзина пуста!</div></div>
  <ConfirmDialog 
    :visible="showConfirm"
    :text="confirmText"
    @confirm="handleConfirm"
  />
</template>

<style scoped>
.cart {
  display: flex;
  position: absolute;
  width: 100%;
  flex-direction: column;
  padding-bottom: 80px;
  gap: 10px;
}

.cart-empty {
  align-content: center;
  position: absolute;
  padding-bottom: 60px;
  height: 100%;
  width: 100%;
  display: block;
  text-align: center;
}

.btn-colored {
    gap: 10px;
    background-color: var(--color-black);
    color: var(--color-white);
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 25px;
    font-weight: bold;
    height: 42px;
    width: 8em;
}

.btn-colored.full-length{
    width: 100%;
}

.disabled{
    opacity: 60%;
    pointer-events: none;
}

</style>