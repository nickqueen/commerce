from typing import List, Optional
from src.models.cart import Cart, CartItem
from src.models.user import db

class CartDAO:
    """Data Access Object para Cart"""
    
    @staticmethod
    def create(user_id: int) -> Cart:
        """Cria um novo carrinho para o usuário"""
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()
        return cart
    
    @staticmethod
    def get_by_user_id(user_id: int) -> Optional[Cart]:
        """Busca carrinho por ID do usuário"""
        return Cart.query.filter_by(user_id=user_id).first()
    
    @staticmethod
    def get_or_create_by_user_id(user_id: int) -> Cart:
        """Busca ou cria carrinho para o usuário"""
        cart = CartDAO.get_by_user_id(user_id)
        if not cart:
            cart = CartDAO.create(user_id)
        return cart
    
    @staticmethod
    def clear_cart(cart: Cart) -> None:
        """Limpa todos os itens do carrinho"""
        CartItem.query.filter_by(cart_id=cart.id).delete()
        db.session.commit()
    
    @staticmethod
    def delete(cart: Cart) -> bool:
        """Deleta um carrinho"""
        try:
            db.session.delete(cart)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

class CartItemDAO:
    """Data Access Object para CartItem"""
    
    @staticmethod
    def create(cart_id: int, product_id: int, quantity: int) -> CartItem:
        """Cria um novo item no carrinho"""
        cart_item = CartItem(
            cart_id=cart_id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
        db.session.commit()
        return cart_item
    
    @staticmethod
    def get_by_cart_and_product(cart_id: int, product_id: int) -> Optional[CartItem]:
        """Busca item específico no carrinho"""
        return CartItem.query.filter_by(
            cart_id=cart_id,
            product_id=product_id
        ).first()
    
    @staticmethod
    def get_by_id(item_id: int) -> Optional[CartItem]:
        """Busca item por ID"""
        return CartItem.query.get(item_id)
    
    @staticmethod
    def update_quantity(cart_item: CartItem, quantity: int) -> CartItem:
        """Atualiza a quantidade de um item"""
        cart_item.quantity = quantity
        db.session.commit()
        return cart_item
    
    @staticmethod
    def delete(cart_item: CartItem) -> bool:
        """Remove um item do carrinho"""
        try:
            db.session.delete(cart_item)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False
    
    @staticmethod
    def add_or_update_item(cart_id: int, product_id: int, quantity: int) -> CartItem:
        """Adiciona item ao carrinho ou atualiza quantidade se já existir"""
        existing_item = CartItemDAO.get_by_cart_and_product(cart_id, product_id)
        
        if existing_item:
            # Item já existe, atualiza quantidade
            existing_item.quantity += quantity
            db.session.commit()
            return existing_item
        else:
            # Item não existe, cria novo
            return CartItemDAO.create(cart_id, product_id, quantity)

