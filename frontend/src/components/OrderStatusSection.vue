<script setup>
import { computed } from 'vue';
import SectionTitle from './SectionTitle.vue';
import { orderStateLables } from '@/store';

const props = defineProps({
    statuses: Array,
    currentStatusId: Number, 
    isCanceled: Boolean,
    isCompleted: Boolean
})


console.log(props.isCanceled, props.isCompleted)

const stateLable = computed(() =>{
    if (props.isCanceled) return orderStateLables.canceled
    else return orderStateLables.completed
})

</script>

<template>
<div class="section top">
    <SectionTitle :title="'Статус заказа'"/>
    <div>
        <div v-if="!isCanceled && !isCompleted" v-for="status in statuses">
            <div class="status-container" :class="{'current-status' : status.id == currentStatusId}">{{ status.name }}</div>
                <hr class="vertical"/>
                <div class="status-description-container" :class="{'current-status' : status.id == currentStatusId}">
                    <img class="icon small" :src="`/icons/${status.icon}`"/>
                    <div>{{ status.description }}</div>
                </div>
                <hr class="vertical"/>
            </div>
        <div class="status-container" :class=" { 'current-status' : isCanceled || isCompleted }">{{ stateLable }}</div>
    </div>
</div>
</template>

<style scoped>
.status-description-container{
  display: flex;
  flex-direction: row;
  gap: 5px;
  align-items: center;
}

.current-status{
  font-weight: bold;
}
</style>