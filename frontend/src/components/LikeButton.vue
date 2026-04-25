<script setup>
import activeIcon from '@/assets/icons/like-active.png'
import inActiveIcon from '@/assets/icons/likes.png'

const emit = defineEmits(['clickLikeBtn']);

const props = defineProps({
    isActive:{
        type: Boolean,
        default: true
    },
    isEnabled:{
        type: Boolean,
        default: true
    }
})

const handleClick = () => {
    emit('clickLikeBtn'); 
}
</script>

<template>
    <div class="btn" :class="{'disabled' : !isEnabled}" @click="handleClick">
        <img class="icon" :src="isActive ? activeIcon : inActiveIcon">
    </div>
</template>

<style scoped>
.icon{
    text-align: center;
    width: 28px;
    height: 28px;
    /* margin: auto; */
}
</style>