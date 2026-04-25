<script setup>

import CartItemCard from '@/components/CartItemCard.vue'
import { getProductWordAccordingToQuantity } from '@/utils/misc'

const props = defineProps({
    items: Array,
    itemsCount: Number,
    fullPrice: Number,
    totalDiscount: Number,
    total: Number,
    updating: Boolean,
    readOnly: Boolean
})

const emit = defineEmits(['syncCount', 'clear'])

</script>

<template>
  <Loading v-if="loading && showLoadingScreen" />
  
    <div class="section" :class="{'top' : !readOnly}">
      <div class="section-sub-col">
        <div class="text big bold">Товары</div>
        <div v-if="!readOnly" class="btn-small" @click="emit('clear')">очистить</div>
      </div>
      <div class="list-container">
        <CartItemCard v-for="item in props.items" :productId="item.product.id" :name="item.product.name"
          :price="item.normal_price ?? item.product.price" :discountPrice="item.purchase_price ?? item.product.discount_price" :img="item.product.img"
          :cartCount="item.quantity" :readOnly="readOnly" @syncCartItemCount="(id, count) => emit('syncCount', id, count)" />
      </div>
    </div>
    <div class="section" :class="{'updating' : props.updating}">
      <div class="text big bold">Сводка о корзине</div>
      <div class="section-sub-col">
        <div class="text small bold">{{ props.itemsCount }} {{ getProductWordAccordingToQuantity(props.itemsCount) }}</div>
        <div class="text small bold dark">{{ props.fullPrice }} ₽</div>
      </div>
      <div>
        <div class="section-sub-col">
          <div class="text small bold">Выгода</div>
          <div class="text small bold" :class="[props.totalDiscount>0 ? 'red' : 'dark']">{{ (0 - props.totalDiscount).toFixed(2) }} ₽</div>
        </div>
      </div>
      <hr/>
      <div class="section-sub-col">
        <div class="text medium bold">Итого</div>
        <div class="text medium bold dark">{{ props.total }} ₽</div>
      </div>
    </div>
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

.section {
  width: 100%;
  background-color: var(--color-bg-secondary);
  display: flex;
  flex-direction: column;
  gap: 15px;
  padding: 15px;
  border-radius: 25px;
}

.section-sub-col {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
}

.section.top {
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}

.btn-small {
  display: flex;
  align-items: center;
  margin-top: 5px;
  margin-bottom: 5px;
  padding: 5px 10px 5px 10px;
  border-radius: 5px;
  font-size: 12px;
  font-weight: bold;
  color: var(--color-red);
}

.list-container {
  width: 100%;
  gap: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
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

.updating {
  opacity: 60%;
}

hr{
    border-color: var(--color-border);
    border-radius: 25px;
    border-style:solid;
    border-top-width: 0.8px;
    border-bottom: none;
}
</style>