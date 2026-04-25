<script setup>
import { ref } from 'vue'

import { getAuthToken } from '@/utils/misc'

import { addItem, decrementItem, incrementItem, deleteItem } from '@/utils/quantityManager'

import Gallery from '@/components/Gallery.vue'
import PriceContainer from '@/components/PriceContainer.vue'
import LikeButton from '@/components/LikeButton.vue'
import SmartCartControls from '@/components/SmartCartControls.vue'


const props = defineProps({
    id: Number
})

var name = ref('')
var price = ref(0.00)
var discountPrice = ref(0.00)
var discount = ref(0)
var album = ref([])
var details = ref(Object)
var loading = ref(true)
var showLoadingScreen = ref(false)
var cartCount = ref(0)
var isOnFavList = ref(false)
var isFavBtnEnabled = ref(true)
var isCartControlsEnabled = ref(true)

fetch(`/api/product?product_id=${props.id}`,{
headers:{
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
    name.value = data.product.name;
    price.value = data.product.price;
    discountPrice.value = data.product.discount_price;
    discount.value = data.product.discount;
    album.value = data.product.album;
    details.value = data.product.details;
    cartCount.value = data.count;
    isOnFavList.value = data.fav_status;
})
.catch(error => {
    console.error('There was a problem with the fetch operation:', error);
})
.finally(() => {
    loading.value = false;
})

function onClickAddToCartBtn(){
    addItem(props.id);
    cartCount.value = 1;
}
// function onClickIncrementCartItemBtn(){
//     cartCount.value = incrementItem(props.id);
// }
async function onClickIncrementCartItemBtn(){
    try {
        isCartControlsEnabled.value = false
        cartCount.value = await incrementItem(props.id)
        console.log('Новое количество в корзине:', cartCount.value)
    }
    catch (error) {
        console.error('Не удалось обновить счетчик корзины:', error)
    }
    finally{
        isCartControlsEnabled.value = true
    }
}

async function onClickDecrementCartItemBtn(){
    if (cartCount.value == 1){
        deleteItem(props.id);
        cartCount.value = 0;
    }
    else{
        try {
            isCartControlsEnabled.value = false
            cartCount.value = await decrementItem(props.id)
            console.log('Новое количество в корзине:', cartCount.value)
        }
        catch (error) {
            console.error('Не удалось обновить счетчик корзины:', error);
        }
        finally{
            isCartControlsEnabled.value = true
        }
    }
}

function onClickLikeBtn(){
    isFavBtnEnabled.value = false;
    var url = '';
    if(isOnFavList.value){
        url = '/api/product/delete_from_fav'
    }
    else{
        url = '/api/product/add_to_fav'
    }
    fetch(`${url}`, {
        method: 'POST',
        headers:{
            'Authorization': `Bearer ${getAuthToken()}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product_id: props.id})
    })
    .then(response =>{
        if (!response.ok) {
            throw new Error('Ошибка')
        }
        return response.json();
    })
    .then(data => {
        isOnFavList.value = data;
    })
    .catch(error =>{
        console.error('Ошибка изменения статуса товара в избранном');
    })
    .finally(() =>{
        isFavBtnEnabled.value = true;
    })
}

setTimeout(()=>{ showLoadingScreen = true }, 300)

</script>

<template>
    <Loading v-if="loading && showLoadingScreen"/>
    <div v-if="!loading" class="product fade-in">
        <div>
        <Gallery :album="album" />
        <div class="section-main">            
                <div class="section-sub-col">
                    <div class="text big dark bold">{{ name }}</div>
                    <LikeButton 
                        :isActive="isOnFavList"
                        :isEnabled="isFavBtnEnabled"
                        @clickLikeBtn="onClickLikeBtn"
                        />
                </div>
                <div class="section-sub-col">
                    <PriceContainer :isProductPage="true" :discountPrice="discountPrice" :normalPrice="price"/>
                    <SmartCartControls 
                        :isEnabled="isCartControlsEnabled"
                        :count="cartCount"
                        @clickAddToCartBtn="onClickAddToCartBtn"
                        @clickIncrementCartItemBtn="onClickIncrementCartItemBtn"
                        @clickDecrementCartItemBtn="onClickDecrementCartItemBtn"
                    />
                </div>
        </div>
        </div>
        <div v-if="details.mainDetails.length > 0 || details.subDetails.length > 0" class="details-container">
            <div class="text big bold section">О товаре</div>
            <div v-if="details.mainDetails.length > 0" class="section">
                <div v-for="detail in details.mainDetails" :key="detail.name" class="product-detail-container">
                    <div class="text xsmall bold gray">{{ detail.name }}</div>
                    <div class="text small bold dark">{{ detail.value }}</div>
                </div>
            </div>
            <hr v-if="details.mainDetails.length > 0 && details.subDetails.length > 0"/>
            <div v-if="details.subDetails.length > 0" class="section">
                <div v-for="detail in details.subDetails" :key="detail.name" class="product-detail-container">
                    <div class="text xsmall bold gray">{{ detail.name }}</div>
                    <div class="text small bold dark">{{ detail.value }}</div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.details-container{
    display: flex;
    flex-direction: column;
    /* gap: 10px; */
    /* margin-top: 10px; */
    background-color: var(--color-bg-secondary);
    border-radius: 25px;
}

.section-main {
    width: 100%;
    background-color: var(--color-bg-secondary);
    display: flex;
    flex-direction:column;
    border-bottom-left-radius: 25px;
    border-bottom-right-radius: 25px;
    padding: 15px;
    gap: 15px;
}

.section-main .section-sub-col {
    /* padding: 10px; */
}

.section-sub-col {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
}

.section {
    width: 100%;
    background-color: var(--color-bg-secondary);
    display: flex;
    flex-direction:column;
    /* gap: 10px; */
    gap: 20px;
    /* padding: 10px; */
    padding: 15px;
    border-radius: 25px;
}

.product-detail-container {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.product{
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.disabled{
    pointer-events: none;
    opacity: 60%;
}

hr{
    /* width: 95%;
    margin: auto; */
    border-color: var(--color-border);
    border-radius: 25px;
    border-style:solid;
    border-top-width: 0.8px;
    border-bottom: none;
}
</style>