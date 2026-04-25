import { getAuthToken } from '@/utils/misc'
import { onMounted, ref } from 'vue'

export function useOrderFetch(orderId) {
    const orderData = ref(null)
    const statusesData = ref(null)
    const loading = ref(true)

    onMounted(fetchOrder)

    function fetchOrder(){
        loading.value = true
        fetch(`/api/order?order_id=${orderId}`,{
            headers: {
            'Authorization': `Bearer ${getAuthToken()}`,
            'Content-Type': 'application/json'
            }
            })
            .then(response =>{
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                orderData.value = data.orderData
                statusesData.value = data.statuses;
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            })
            .finally(() => {
                loading.value = false;
            })
    }

    return {  loading, orderData, statusesData, refetch: fetchOrder }
}