import { appWarehouse } from "@/store";

export function getProductWordAccordingToQuantity(quantity){
    if (quantity % 100 >= 11 && quantity % 100 <= 14) {
        return "товаров";
    }
    const lastDigit = quantity % 10;
    if (lastDigit === 1) return "товар";
    if (lastDigit >= 2 && lastDigit <= 4) return "товара";
    return "товаров";
}

export function getAuthToken(){
    const token = document.cookie
        .split('; ')
        .find(row => row.startsWith('access_token='))
        ?.split('=')[1];
    return token;
}

export function getInitData(){
  fetch('/api/init',{
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
      appWarehouse.setCount(data.items_count)
  })
  .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
  })
  .finally(() => {
  })
}