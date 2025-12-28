import { useContext } from 'react';
import { CartContext } from '../context/CartContext';

export const useCart = () => {
    const context = useContext(CartContext);
    if (!context) {
        throw new Error('useCart must be used inside CartProvider');
    }
    const addToCart = async (product, quantity = 1) => {
        await context.addToCart(product.ID, quantity);
    };

    const incrementItem = async (product, quantity = 1) => {
        await context.incrementItem(product.EntityID, quantity);
    };

    const decrementItem = async (product, quantity = 1) => {
        console.log('DECREMENT ITEM PAYLOAD', {
        entity_id: product.EntityID,
        quantity: quantity
    });
        const response = await context.decrementItem(product.EntityID, quantity);
        console.log('DECREMENT RESPONSE', response);
    };

    const removeItem = async (product, quantity = 1) => {
        const response = await context.removeItem(product.EntityID, quantity);
        console.log('REMOVE ITEM RESPONSE', response);
    };

    return {
        ...context,
        addToCart,
        incrementItem,
        decrementItem,
        removeItem,
    };
};
