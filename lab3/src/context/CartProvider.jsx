import { useState, useEffect } from 'react';
import { CartContext } from './CartContext';
export const CartProvider = ({ children }) => {
    const [cart, setCart] = useState(() => {
        const saved = localStorage.getItem('cart');
        return saved ? JSON.parse(saved) : [];
    });

    useEffect(() => {
        localStorage.setItem('cart', JSON.stringify(cart));
    }, [cart]);

    const addToCart = (product) => {
        setCart(prev => {
            const existing = prev.find(item => item.ID === product.ID);

            if (existing) {
                return prev.map(item =>
                    item.ID === product.ID
                        ? { ...item, quantity: item.quantity + 1 }
                        : item
                );
            }

            return [
                ...prev,
                {
                    ID: product.ID,
                    Title: product.Title,
                    Price: product.Price,
                    quantity: 1,
                    ImageURL: product.Images?.[0]?.ImageURL
                }
            ];
        });
    };

    const decreaseQuantity = (productId) => {
        setCart(prev =>
            prev
                .map(item =>
                    item.ID === productId
                        ? { ...item, quantity: item.quantity - 1 }
                        : item
                )
                .filter(item => item.quantity > 0)
        );
    };

    const removeFromCart = (productId) => {
        setCart(prev => prev.filter(item => item.ID !== productId));
    };

    const clearCart = () => setCart([]);

    const totalCount = cart.reduce((sum, item) => sum + item.quantity, 0);
    const totalPrice = cart.reduce(
        (sum, item) => sum + Number(item.Price) * item.quantity,
        0
    );

    return (
        <CartContext.Provider
            value={{
                cart,
                addToCart,
                decreaseQuantity,
                removeFromCart,
                clearCart,
                totalCount,
                totalPrice
            }}
        >
            {children}
        </CartContext.Provider>
    );
};
