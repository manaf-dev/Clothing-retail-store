import { defineStore } from 'pinia';
import { orderService } from '@/services/orderService.js';

export const usePOSStore = defineStore('pos', {
  state: () => ({
    currentOrder: {
      items: [],
      customer_name: '',
      total: 0,
      status: 'pending'
    },
    cart: [],
    selectedProduct: null,
    loading: false,
    error: null
  }),

  getters: {
    cartTotal: (state) => {
      return state.cart.reduce((total, item) => {
        return total + (item.price * item.quantity);
      }, 0);
    },

    cartItemCount: (state) => {
      return state.cart.reduce((total, item) => total + item.quantity, 0);
    }
  },

  actions: {
    addToCart(product, quantity = 1) {
      const existingItem = this.cart.find(item => item.product_id === product.id);
      
      if (existingItem) {
        existingItem.quantity += quantity;
      } else {
        this.cart.push({
          product_id: product.id,
          product_name: product.name,
          price: product.price,
          quantity: quantity,
          size: product.size || 'M',
          color: product.color || 'Default'
        });
      }
    },

    removeFromCart(productId) {
      const index = this.cart.findIndex(item => item.product_id === productId);
      if (index > -1) {
        this.cart.splice(index, 1);
      }
    },

    updateCartItemQuantity(productId, quantity) {
      const item = this.cart.find(item => item.product_id === productId);
      if (item) {
        if (quantity <= 0) {
          this.removeFromCart(productId);
        } else {
          item.quantity = quantity;
        }
      }
    },

    clearCart() {
      this.cart = [];
      this.currentOrder.customer_name = '';
    },

    async processOrder(customerName = '') {
      this.loading = true;
      try {
        const orderData = {
          customer_name: customerName,
          status: 'completed',
          total: this.cartTotal,
          payment_method: 'cash',
          items: this.cart.map(item => ({
            product_id: item.product_id,
            quantity: item.quantity,
            price: item.price
          }))
        };
        console.log('Processing order:', orderData);

        const response = await orderService.createOrder(orderData);
        this.clearCart();
        return response.data;
      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.loading = false;
      }
    }
  }
});
