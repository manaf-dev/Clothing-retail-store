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
        // Check if we can add more quantity
        const newQuantity = existingItem.quantity + quantity;
        if (newQuantity <= product.stock) {
          existingItem.quantity = newQuantity;
        } else {
          throw new Error(`Cannot add more items. Only ${product.stock} available.`);
        }
      } else {
        if (quantity <= product.stock) {
          this.cart.push({
            product_id: product.id,
            product_name: product.name,
            price: product.effective_price || product.price,
            quantity: quantity,
            stock: product.stock
          });
        } else {
          throw new Error(`Cannot add ${quantity} items. Only ${product.stock} available.`);
        }
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
        } else if (quantity <= item.stock) {
          item.quantity = quantity;
        } else {
          throw new Error(`Cannot set quantity to ${quantity}. Only ${item.stock} available.`);
        }
      }
    },

    clearCart() {
      this.cart = [];
    },

    async processOrder(orderData) {
      try {
        this.loading = true;
        this.error = null;

        // Create order using the order service
        const order = await orderService.createOrder({
          customer_name: orderData.customer_name || '',
          payment_method: orderData.payment_method,
          tax_amount: orderData.tax_amount || 0,
          discount_amount: orderData.discount_amount || 0,
          items: orderData.items,
          status: 'completed',  // Mark POS orders as completed immediately
          payment_status: 'paid',
          served_by: 'POS System'
        });

        // Clear cart on success
        this.clearCart();
        
        return order;
      } catch (error) {
        this.error = error.message || 'Failed to process order';
        throw error;
      } finally {
        this.loading = false;
      }
    }
  }
});
