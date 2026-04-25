import { reactive } from "vue";

export const appWarehouse = reactive({

    cartCount: 0,
    setCount(val){
        this.cartCount = val
    }
})

export const orderStateLables = {
    canceled: 'отменен',
    completed: 'завершен'
}