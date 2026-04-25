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
            throw new Error('Ошибка')
        }
        return response.json();
    })
    .then(data => {
        getInitData()
        return data
    })
    .catch(error =>{
        console.error('Ошибка добавления отвара в корзину');
    });
}

export function decrementItem(productId, count){
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
            throw new Error('Ошибка')
        }
        return response.json();
    })
    .then(data => {
        getInitData()
        return data
    })
    .catch(error =>{
        console.error('Ошибка добавления отвара в корзину');
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
            throw new Error('Ошибка')
        }
        return response.json();
    })
    .then(data => {
        getInitData()
        return 1
    })
    .catch(error =>{
        console.error('Ошибка добавления отвара в корзину');
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
            throw new Error('Ошибка')
        }
        return response.json();
    })
    .then(data => {
        getInitData()
        return 0
    })
    .catch(error =>{
        console.error('Ошибка добавления отвара в корзину');
    });
}