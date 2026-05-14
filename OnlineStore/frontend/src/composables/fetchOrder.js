import { getAuthToken } from '@/utils/misc'
import { onMounted, ref } from 'vue'

export function useOrderFetch(orderId) {
    const orderData = ref(null)
    const statusesData = ref(null)
    const loading = ref(true)

    onMounted(fetchOrder)

    function fetchOrder(){
        loading.value = true
        fetch(`/api/orders/order?order_id=${orderId}`,{
            headers: {
            'Authorization': `Bearer ${getAuthToken()}`,
            'Content-Type': 'application/json'
            }
            })
            .then(response =>{
                if (!response.ok) {
                    if (response.status === 401) {
                        throw new Error('Unauthorized access')
                    }
                    else if (response.status === 403) {
                        throw new Error('Forbidden')
                    }
                    else if (response.status === 404) {
                        throw new Error('Order not found')
                    }
                    throw new Error('Server error')
                }
                return response.json();
            })
            .then(data => {
                orderData.value = data.orderData
                statusesData.value = data.statuses
            })
            .catch(error => {
                console.error('Fetch order failed:', error)
            })
            .finally(() => {
                loading.value = false
            })
    }

    return {  loading, orderData, statusesData, refetch: fetchOrder }
}