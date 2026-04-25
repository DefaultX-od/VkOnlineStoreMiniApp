<script setup>
import homeIcon from '@/assets/icons/home.png'
import catalogIcon from '@/assets/icons/catalog.png'
import likesIcon from '@/assets/icons/likes.png'
import cartIcon from '@/assets/icons/cart.png'
import ordersIcon from '@/assets/icons/orders.png'

import homeActiveIcon from '@/assets/icons/home-active.png'
import catalogActiveIcon from '@/assets/icons/catalog-active.png'
import likesActiveIcon from '@/assets/icons/likes-active.png'
import cartActiveIcon from '@/assets/icons/cart-active.png'
import ordersActiveIcon from '@/assets/icons/orders-active.png'

import FooterButton from '@/components/FooterButton.vue'

const buttons = [
    {
        label: 'Главная',
        link: '/',
        activeIcon: homeActiveIcon,
        inactiveIcon: homeIcon,
    },
    {
        label: 'Каталог',
        link: '/catalog',
        activeIcon: catalogActiveIcon,
        inactiveIcon: catalogIcon,
    },
    {
        label: 'Избранное',
        link: '/favorites',
        activeIcon: likesActiveIcon,
        inactiveIcon: likesIcon,
    },
    {
        label: 'Корзина',
        link: '/cart',
        activeIcon: cartActiveIcon,
        inactiveIcon: cartIcon,
        noteName: 'cartCount'
    },
    {
        label: 'Заказы',
        link: '/orders',
        activeIcon: ordersActiveIcon,
        inactiveIcon: ordersIcon
    }
]
</script>

<template>
    <nav class="footer" id="footer">
        <FooterButton 
        v-for="(button, index) in buttons" 
        :key="index" 
        :label="button.label"
        :link="button.link"
        :active-icon="button.activeIcon"
        :inactive-icon="button.inactiveIcon"
        :disabled="button.disabled"
        :noteName="button.noteName"
        />
    </nav>
</template>

<style scoped>
.footer {
    background-color: var(--color-bg-primary);
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    margin: 10px;
    display: flex;
    justify-content: space-around;
    padding: 5px 5px;
    z-index: 10;
    border-radius: 25px;
    box-shadow: 0 0 5px 5px var(--color-shadow);
}

@supports (backdrop-filter: blur(10px)) {
    .footer {
        background: var(--color-bg-primary-semi-transparent);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }
}
@supports (-webkit-backdrop-filter: blur(10px)) {
    .footer {
        background: var(--color-bg-primary);
    }
}
</style>