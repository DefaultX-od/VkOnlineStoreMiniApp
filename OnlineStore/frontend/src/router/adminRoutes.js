import AdminDashboardView from '@/views/AdminDashboardView.vue'
import OrderAdminView from '@/views/OrderAdminView.vue'
import OrdersAdminView from '@/views/OrdersAdminView.vue'

export const admintRoutes = [
    {
        path: '/',
        name: 'adminDashboard',
        component: AdminDashboardView,
        meta: { hideFooter: true }
    },
    {
        path: '/orders/:status_id',
        name: 'adminOrders',
        component: OrdersAdminView,
        meta: { hideFooter: true },
        props: true
    },
    {
        path: '/orders/canceled',
        name: 'adminOrdersCanceled',
        component: OrdersAdminView,
        meta: { hideFooter: true },
        props: { is_canceled: true }
    },
    {
        path: '/orders/completed',
        name: 'adminOrdersCompleted',
        component: OrdersAdminView,
        meta: { hideFooter: true },
        props: { is_completed: true }
    },
    {
        path: '/orders/order/:id',
        name: 'order',
        props: true,
        component: OrderAdminView,
        meta: { hideFooter: true }
    }
] 