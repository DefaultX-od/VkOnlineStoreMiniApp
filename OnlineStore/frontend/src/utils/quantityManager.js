import { getAuthToken, getInitData } from './misc.js'

export function incrementItem(productId){
    return fetch('/api/cart/item/increment', {
        method: 'POST',
        headers:{
            'Authorization': `Bearer ${getAuthToken()}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product_id: productId})
    })
    .then(response =>{
        if (!response.ok) {
            if (response.status === 401) {
                throw new Error('Unauthorized access')
            }
            throw new Error('Server error')
        }
        return response.json()
    })
    .then(data => {
        getInitData()
        return data
    })
    .catch(error =>{
        console.error('Error item increment', error);
    });
}

export function decrementItem(productId){
    return fetch('/api/cart/item/decrement', {
        method: 'POST',
        headers:{
            'Authorization': `Bearer ${getAuthToken()}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product_id: productId})
    })
    .then(response =>{
        if (!response.ok) {
            if (response.status === 401) {
                throw new Error('Unauthorized access')
            }
            throw new Error('Server error')
        }
        return response.json()
    })
    .then(data => {
        getInitData()
        return data
    })
    .catch(error =>{
        console.error('Error item decrement', error)
    });
}

export function addItem(productId){
    fetch('/api/cart/item/add', {
        method: 'POST',
        headers:{
            'Authorization': `Bearer ${getAuthToken()}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product_id: productId})
    })
    .then(response =>{
        if (!response.ok) {
            if (response.status === 401) {
                throw new Error('Unauthorized access')
            }
            throw new Error('Server error')
        }
        return response.json()
    })
    .then(data => {
        getInitData()
        return 1
    })
    .catch(error =>{
        console.error('Error add item', error)
    });
}

export function deleteItem(productId){
    return fetch('/api/cart/item/delete', {
        method: 'POST',
        headers:{
            'Authorization': `Bearer ${getAuthToken()}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product_id: productId})
    })
    .then(response =>{
        if (!response.ok) {
            if (response.status === 401) {
                throw new Error('Unauthorized access')
            }
            throw new Error('Server error')
        }
        return response.json()
    })
    .then(data => {
        getInitData()
        return 0
    })
    .catch(error =>{
        console.error('Error delete item', error)
    });
}