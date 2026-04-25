<script setup>
import SectionTitle from './SectionTitle.vue';


const props = defineProps({
    paymentMethod : Object,
    dropPoint : Object
})

</script>

<template>
<div class="section">
    <SectionTitle :title="'Пункт вывоза и способ оплаты'"/>
    <div class="text small bold">Заказ будет ждать</div>
    <div class="detail-description-container">
        <img class="icon small" :src="`/icons/map-pin.png`">
        <div>{{ dropPoint.text }}</div>
    </div>
    <hr/>
    <div class="text small bold">Способ оплаты</div>
    <div class="detail-description-container">
        <img class="icon small" :src="`/icons/${paymentMethod.icon}`">
        <div>{{ paymentMethod.text }}</div>
    </div>
</div>
</template>

<style scoped>
.detail-description-container{
  display: flex;
  flex-direction: row;
  gap: 5px;
  align-items: center;
}
hr{
    border-color: var(--color-border);
    border-radius: 25px;
    border-style:solid;
    border-top-width: 0.8px;
    border-bottom: none;
}
</style>