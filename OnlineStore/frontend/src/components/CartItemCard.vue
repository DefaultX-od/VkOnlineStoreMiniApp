<script setup>
import { computed, ref } from 'vue'
import { incrementItem, decrementItem, deleteItem } from '@/utils/quantityManager'
import PriceContainer from './PriceContainer.vue'
import SmartCartControls from './SmartCartControls.vue'
import imagePlaceholder from '@/assets/icons/no-img.png'
import deleteIcon from '@/assets/icons/close.png'

const emit = defineEmits([
    'syncCartItemCount'
])

var cartControlsEnabled = ref(true)

const props = defineProps({
    productId: Number,
    name: String,
    price: Number,
    discountPrice: Number,
    img: String,
    cartCount: Number,
    readOnly: Boolean
})

const validSrc = computed (() => props.img && props.img !== null ? props.img : imagePlaceholder)

function onClickIncrementCartItemBtn(){
    cartControlsEnabled.value = false;
    incrementItem(props.productId)
    .then(newCount => {
        emit('syncCartItemCount', props.productId, newCount);
    })
    .finally(()=>{
            cartControlsEnabled.value = true;
    });
}
function onClickDecrementCartItemBtn(){
    cartControlsEnabled.value = false;
    if (props.cartCount == 1){
        deleteItem(props.productId)
        .then(newCount => {
            emit('syncCartItemCount', props.productId, newCount);
        })
        .finally(()=>{
            cartControlsEnabled.value = true;
        });
    }
    else{
        decrementItem(props.productId)
        .then(newCount => {
            emit('syncCartItemCount', props.productId, newCount);
        })
        .finally(()=>{
            cartControlsEnabled.value = true;
        });
    }   

}
function onClickDeleteCartItemBtn(){
    cartControlsEnabled.value = false;
    deleteItem(props.productId)
    .then(newCount => {
        emit('syncCartItemCount', props.productId, newCount);
    });
}

</script>

<template>
    <div v-if="cartCount > 0" class="list-object">
        <div class="list-object-img-container">
            <img referrerpolicy="no-referrer" :src="validSrc">
        </div>
        <div class="list-object-details">
            <div class="product-name">{{ name }}</div>
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div v-if="readOnly">{{ cartCount }} шт.</div>
                <PriceContainer :discountPrice="discountPrice" :normalPrice="price"/>
            </div>
            <div v-if="!readOnly" class="item-tools-container" :class="{'disabled' : !cartControlsEnabled}">
                <div class="flat-btn left-corner" @click="onClickDeleteCartItemBtn">
                    <img class="icon tiny" :src="deleteIcon">
                </div>
                <SmartCartControls 
                    :count="cartCount"
                    @clickIncrementCartItemBtn="onClickIncrementCartItemBtn"
                    @clickDecrementCartItemBtn="onClickDecrementCartItemBtn" 
                />
            </div>
        </div>
    </div>
</template>

<style scoped>
.product-name{
    font-size: 14px;
    font-weight: bold;
    overflow: hidden;
    position: relative;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    color: var(--color-text-secondary);
    line-height: 1.1;
}

.list-object {
    width: 100%;
    display: flex;
    background-color: var(--color-bg-secondary);
    border-radius: 15px;
    gap: 15px;
    padding: 5px;
    align-items: center;
    align-items: stretch;
}
.list-object-img-container{
    width: 100px;
    height:100px;
    align-content: center;
    border-radius: 15px;
    display: flex;
    align-items: center;
}

.list-object-img-container img{
    object-fit: contain;
    width: inherit;
    height: inherit;
    border-radius: 15px;
    margin-left: 0;
    vertical-align: middle;
}
.item-tools-container{
    font-size: 14px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}
.flat-btn{
    display: flex;
    align-items: center;
    padding: 10px;
}

.flat-btn.left-corner{
    padding-left: 0;
}
.list-object-details{
    display: flex;
    flex-direction: column;
    width: 100%;
    justify-content: space-between; 
}
.icon {
    width: 24px;
    height: 24px;
    text-align: center;
}

.icon.tiny{
    width: 14px;
    height: 14px;
}

.disabled{
    pointer-events: none;
    opacity: 60%;
}
</style>