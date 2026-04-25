<script setup>
import { RouterLink, useRoute } from 'vue-router'
import { computed } from 'vue'
import { appWarehouse } from '@/store';

const props = defineProps({
  link: String,
  label: String,
  activeIcon: String,
  inactiveIcon: String,
  disabled: Boolean,
  noteName: String
})

const route = useRoute();
const isActive = computed(() => {
    if (props.link === '/') {
        return route.path === props.link;
    }
    return route.path.startsWith(props.link);
})
</script>

<template>
    <RouterLink 
    :to="disabled? '#' : link"
    class="footer-button"
    :class="{'disabled' : disabled, 'active' : isActive}"
    :event="disabled ? '' : 'click'">
        <div v-if="noteName && appWarehouse[noteName]" class="note text light tiniest">{{ appWarehouse[noteName] }}</div>
        <img class="icon-small" :src="isActive ? activeIcon : inactiveIcon">
        <div class="text tiny">{{ label }}</div>
    </RouterLink>
</template>


<style scoped>
.footer-button {
    width: 20%;
    padding: 6px 0px;
    border-radius: 25px;
    display: flex;
    position: relative;
    flex-direction: column;
    align-items: center;
    gap: 2px;
    cursor: pointer;
    background-color: transparent;
    transition: background-color 0.3s ease;
    -webkit-tap-highlight-color: transparent;
}

.active {
    background-color: var(--color-accent-semi-transparent);
    font-weight: bold;
}

.disabled {
    pointer-events: none;
    opacity: 60%;
}
.note{
    position: absolute;
    opacity: 90%;
    min-width: 3.3ch;
    text-align: center;
    right: 15px;
    top: 3px;
    padding: 2px;
    font-weight: bold;
    border-radius: 10px;
    background-color: var(--color-red);
}
</style>