<script setup>

const emit = defineEmits(['confirm'])

const props = defineProps({
    text: String,
    visible: Boolean
})

const handleClick = (val) => {
    emit('confirm', val)
}
</script>

<template>
    <div v-if="visible" class="overlay">
        <div class="dialog-body">
            <div class="message-text text big bold">{{ text }}</div>
            <div class="dialog-button-group">
            <div class="dialog-button text medium" @click="handleClick(true)">Да</div>
            <div class="dialog-button text medium" @click="handleClick(false)">Отмена</div>
        </div>
        </div>
    </div>  
</template>

<style scoped>
.overlay{
    background-color: var(--color-border);
    height: 100%;
    width: 100%;
    display: flex;
    position: absolute;
    align-items: center;
    margin: auto;
    gap: 10;
    flex-direction: column;
    z-index: 11;
}
.dialog-body{
    width: 85%;
    position: absolute;
    top: 30%;
    padding: 5px;
    display: flex;
    flex-direction: column;
    /* gap: 10px; */
    background-color: var(--color-bg-primary);
    border-radius: 25px;
}
.message-text{
    width: 100%;
    padding: 30px;
    text-align: center;
}
.dialog-button-group{
    width: 100%;
    padding: 5px;
    display: flex;
    flex-direction: row;
    border-radius: inherit;
    gap: 10px;
}
.dialog-button{
    width: 50%;
    padding: 15px;
    text-align: center;
    border-radius: inherit;
    background-color: var(--color-bg-tertiary);
}
</style>