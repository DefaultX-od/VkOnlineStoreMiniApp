<script setup>
import plusIcon from '@/assets/icons/plus.png'
import minusIcon from '@/assets/icons/minus.png'
import addToCartIcon from '@/assets/icons/cart.png'

const emit = defineEmits([
    'clickAddToCartBtn',
    'clickDecrementCartItemBtn',
    'clickIncrementCartItemBtn'
])

const props = defineProps({
    count:{
        type: Number,
        default: 0
    },
    isEnabled:{
        type: Boolean,
        default: true
    }
})

const handleAdd = () => emit('clickAddToCartBtn');
const handleIncrement = () => emit('clickIncrementCartItemBtn');
const handleDecrement = () => emit('clickDecrementCartItemBtn');
</script>

<template>
<div v-if="count === 0" class="btn-colored" :class="{'disabled' : !isEnabled}" @click="handleAdd">
    <div class="semi-medium bold">В корзину</div>
</div>
<div v-else class="counter" :class="{'disabled' : !isEnabled}">
    <div class="flat-btn" @click="handleDecrement">
        <img class="icon tiny" :src="minusIcon">
        
    </div>
    <div class="display semi-medium bold">{{ count }}</div>
    <div class="flat-btn" @click="handleIncrement">
        <img class="icon tiny" :src="plusIcon">
    </div>
</div>
</template>

<style scoped>
.counter{
    display: flex;
    flex-direction: row;
    border-radius: 25px;
    background-color: var(--color-bg-tertiary);
    justify-content: space-between;
    align-items: center;
    height: 42px;
    width: 8em;
}

.flat-btn{
    padding: 10px;
}

.btn-colored {
    gap: 10px;
    background-color: var(--color-green);
    color: var(--color-white);
    display: inline;
    text-align: center;
    align-content: center;
    border-radius: 25px;
    padding: 8px;
    font-weight: bold;
    height: 42px;
    width: 8em;
}

.btn-colored.flat{
    background-color: var(--color-bg-tertiary);
    color: var(--color-text-secondary);
}
.icon {
    width: 24px;
    height: 24px;
}

.icon.tiny{
    width: 14px;
    height: 14px;
}

.display{
    color: var(--color-text-primary);
}
</style>