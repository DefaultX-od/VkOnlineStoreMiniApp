import HomeView from '@/views/HomeView.vue'
import CategoriesView from '@/views/CategoriesView.vue'
import CategoryView from '@/views/CategoryView.vue'
import ProductGroupView from '@/views/ProductGroupView.vue'
import ProductView from '@/views/ProductView.vue'
import FavoritesView from '@/views/FavoritesView.vue'
import CartView from '@/views/CartView.vue'
import OrdersView from '@/views/OrdersView.vue'
import CheckoutView from '@/views/CheckoutView.vue'
import OrderView from '@/views/OrderView.vue'

export const userRoutes = [
    {
        path: '/',
        name: 'home',
        component: HomeView,
        meta: { hideFooter: false }
    },
    {
        path: '/catalog',
        name: 'catalog',
        component: CategoriesView,
        meta: { hideFooter: false }
    },
    {
        path: '/catalog/category/:id',
        name: 'category',
        props: true,
        component: CategoryView,
        meta: { hideFooter: false }
    },
    {
        path: '/catalog/category/:category_id/group/:group_id',
        name: 'group',
        props: true,
        component: ProductGroupView,
        meta: { hideFooter: false }
    },
    {
        path: '/catalog/product/:id',
        name: 'product',
        props: true,
        component: ProductView,
        meta: { hideFooter: false }
    },
    {
        path: '/favorites',
        name: 'favorites',
        component: FavoritesView,
        meta: { hideFooter: false }
    },
    {
        path: '/cart',
        name: 'cart',
        component: CartView,
        meta: { hideFooter: false }
    },
    {
        path: '/cart/checkout',
        name: 'checkout',
        component: CheckoutView,
        meta: { hideFooter: true }
    },
    {
        path: '/orders',
        name: 'orders',
        component: OrdersView,
        meta: { hideFooter: false }
    },
    {
        path: '/orders/order/:id',
        name: 'order',
        props: true,
        component: OrderView,
        meta: { hideFooter: false }
    }
]