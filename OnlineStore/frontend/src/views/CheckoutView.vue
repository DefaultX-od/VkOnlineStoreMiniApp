<script setup>
    import { onMounted, ref } from 'vue';
    import SectionTitle from '@/components/SectionTitle.vue';
    import { getAuthToken, getInitData } from '@/utils/misc';
    import SmartInputOptionButton from '@/components/SmartInputOptionButton.vue';
    import { useRouter } from 'vue-router';
    
    const router = useRouter()
    var paymentMethods = ref([])
    var dropPoints = ref([])
    var loading = ref(true)

    const selectedPaymentMethod = ref(null)
    const selectedDropPoint = ref(null)

    onMounted(() =>{
        fetchOptions()
    })

    function fetchOptions(){
        fetch('/api/checkout/options',{
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
            paymentMethods.value = data.paymentMethods
            dropPoints.value = data.dropPoints
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error)
        })
        .finally(() =>{
            loading.value = false
        })
    }

    function checkout(){
        fetch('/api/checkout',{
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${getAuthToken()}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'DP': selectedDropPoint.value,
                'PM': selectedPaymentMethod.value
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok')
            }
            return response.json()
        })
        .then(data => {
            getInitData()
            router.replace(`/orders/order/${data.order_id}`)
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error)
        })
        .finally(() =>{
            loading.value = false
        })
    }
</script>

<template>
    <div class="checkout">
        <div class="text small bold dark" style="text-align: center; width: 100%;">Оформление заказа</div>
        <SectionTitle :title="'Способ оплаты'"/>
        <form id="payment-methods" class="grid-container">
            <div v-for="item in paymentMethods" :key="item.id" class="grid-object radio-btn column-template">
                <SmartInputOptionButton :item="item" :parentForm="'paymentMethods'" v-model:selectedModel="selectedPaymentMethod"/>
            </div>
        </form>
        <SectionTitle :title="'Пункт выдачи заказа'"/>
        <form id="drop-points" class="flex-row" style="overflow-y: auto;">
            <div v-for="item in dropPoints" :key="item.id" class="radio-btn">
                <SmartInputOptionButton :item="item" :parentForm="'droppoints'" v-model:selectedModel="selectedDropPoint"/>
            </div>
        </form>
        <div @click="checkout" class="btn-colored full-length" :class="{ 'disabled': !selectedPaymentMethod || !selectedDropPoint }" id="create-order-btn">
            <div class="label">Оформить</div>
        </div>
    </div>
</template>

<style scoped>
.checkout{
  width: 95%;
  margin: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.flex-row{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
}

.column-container{
    flex-direction: column;
    gap: 5px;
    display: flex;
}
.icon {
    width: 24px;
    height: 24px;
    text-align: center;
}
.grid-container{
    /* margin: 0 auto; */
    display: grid;
    grid-template-columns: 
        calc(50% - var(--gap)/2) 
        calc(50% - var(--gap)/2);
    gap: var(--gap);
    --gap: 8px;
}

.grid-object {
    position: relative;
    display: inherit;
    gap: 5px;
    border-radius: 15px;
    padding: 8px;
    /* margin: 5px; */
    background-color: #fff;
}
.radio-btn {
    position: relative;
    display: block;
    height: fit-content;
    width: 100%;
    /* text-align:center; */
}

.radio-btn .column-template{
    display: flex;
    flex-direction: column;
    gap: 5px;
    align-items: center;
    align-content: center;
}

.grid-object.radio-btn {
    padding: 0px;
    margin: 0;
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
    /* height: 100%; */
}

.disabled{
    pointer-events: none;
    opacity: 60%;
}

/* .radio-btn label {
    display: block;
    background:#EAEAEA;
    border-radius: 8px;
    padding: 10px 10px;
    cursor: pointer;
    font-family:Arial, Helvetica, sans-serif;
} */
</style>