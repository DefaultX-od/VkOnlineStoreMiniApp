<script setup>
import Grid from '@/components/Grid.vue';
import GridObject from '@/components/GridObject.vue';
import { getAuthToken } from '@/utils/misc';
import { onMounted, ref } from 'vue';

var statuses = ref([])

function fetchAdminInitData(){
    fetch('/api/admin/init',{
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
        statuses.value = data.statuses
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error)
    })
    .finally(() =>{
        loading.value = false
    })
}

onMounted(() =>{
    fetchAdminInitData()
})



const orderStates = [
    {
        name: 'Завершенные заказы',
        link: '/orders/completed',
        icon: '/icons/order-completed.png'
    },
    {
        name: 'Отмененные заказы',
        link: '/orders/canceled',
        icon: '/icons/order-canceled.png'
    }

]

</script>
<template>
    <div class="dashboard">
        <Grid>
            <GridObject v-for="status in statuses"
            :text="status.name"
            :link="`/orders/${status.id}`"
            :image="`/icons/${status.icon}`"
            :iconSymbolic="true"
            />
            <GridObject v-for="orderState in orderStates"
            :text="orderState.name"
            :link="orderState.link"
            :image="orderState.icon"
            :iconSymbolic="true"
            />          
        </Grid>
    </div>
</template>
<style>
.dashboard{
    width: 95%;
    margin: auto;
}
</style>