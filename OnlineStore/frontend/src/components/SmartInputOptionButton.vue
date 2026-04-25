<script setup>
    const props = defineProps({
        item: Object,
        parentForm: String
    })
    const model = defineModel('selectedModel');
</script>

<template>
    <input
    type="radio"
    :id = "`${parentForm}Option${item.id}`"
    :name = "parentForm"
    :value="item.id"
    required="true"
    v-model="model"
    />
    <label :for="`${parentForm}Option${item.id}`">
        <div class="flex-row">
            <img 
            v-if="item.icon" 
            :src="`/icons/${item.icon}`" 
            class="icon" 
            alt=""
            />
            {{ item.text }}
        </div>
    </label>
</template>

<style scoped>
label {
    display: block;
    background: #EAEAEA; /* Серый по умолчанию */
    border-radius: 8px;
    padding: 10px 10px;
    cursor: pointer;
    font-family: Arial, Helvetica, sans-serif;
    transition: background-color 0.2s; /* Для плавности */
}
.flex-row{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
}
input[type="radio"] {
    display: none;
    position: absolute;
    width: 100%;
    appearance: none;
}
input[type="radio"]:checked + label {
    background-color: rgba(84, 150, 79, 0.3);
    font-weight: bold;
    /* color:#fff; */
}
</style>