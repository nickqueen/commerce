from dataclasses import dataclass
from typing import List, Optional

@dataclass
class CartItemAddDTO:
    """DTO para adicionar item ao carrinho"""
    product_id: int
    quantity: int = 1

@dataclass
class CartItemUpdateDTO:
    """DTO para atualizar item do carrinho"""
    quantity: int

@dataclass
class CartItemDTO:
    """DTO para item do carrinho"""
    id: int
    product_id: int
    product_name: str
    product_price: float
    product_image_url: Optional[str]
    quantity: int
    subtotal: float
    
    @classmethod
    def from_cart_item(cls, cart_item):
        """Cria DTO a partir do modelo CartItem"""
        return cls(
            id=cart_item.id,
            product_id=cart_item.product_id,
            product_name=cart_item.product.name,
            product_price=float(cart_item.product.price),
            product_image_url=cart_item.product.image_url,
            quantity=cart_item.quantity,
            subtotal=float(cart_item.get_subtotal())
        )

@dataclass
class CartDTO:
    """DTO para carrinho"""
    id: int
    user_id: int
    items: List[CartItemDTO]
    total: float
    item_count: int
    
    @classmethod
    def from_cart(cls, cart):
        """Cria DTO a partir do modelo Cart"""
        return cls(
            id=cart.id,
            user_id=cart.user_id,
            items=[CartItemDTO.from_cart_item(item) for item in cart.items],
            total=float(cart.get_total()),
            item_count=cart.get_item_count()
        )

