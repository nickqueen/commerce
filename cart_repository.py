from typing import Optional
from src.dao.cart_dao import CartDAO, CartItemDAO
from src.dao.product_dao import ProductDAO
from src.models.cart import Cart, CartItem
from src.dto.cart_dto import CartItemAddDTO, CartItemUpdateDTO, CartDTO

class CartRepository:
    """Repository para operações de carrinho usando o padrão Repository"""
    
    def __init__(self):
        self.cart_dao = CartDAO()
        self.cart_item_dao = CartItemDAO()
        self.product_dao = ProductDAO()
    
    def get_user_cart(self, user_id: int) -> Cart:
        """Busca ou cria carrinho para o usuário"""
        return self.cart_dao.get_or_create_by_user_id(user_id)
    
    def add_item_to_cart(self, user_id: int, item_dto: CartItemAddDTO) -> CartItem:
        """Adiciona item ao carrinho"""
        # Validações
        if item_dto.quantity <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        
        # Verificar se produto existe e está ativo
        product = self.product_dao.get_by_id(item_dto.product_id)
        if not product or not product.is_active:
            raise ValueError("Produto não encontrado ou inativo")
        
        # Verificar disponibilidade
        if not product.is_available(item_dto.quantity):
            raise ValueError(f"Produto não disponível na quantidade solicitada. Estoque: {product.stock}")
        
        # Buscar ou criar carrinho
        cart = self.get_user_cart(user_id)
        
        # Adicionar ou atualizar item
        return self.cart_item_dao.add_or_update_item(
            cart.id, 
            item_dto.product_id, 
            item_dto.quantity
        )
    
    def update_cart_item(self, user_id: int, item_id: int, item_dto: CartItemUpdateDTO) -> Optional[CartItem]:
        """Atualiza quantidade de item no carrinho"""
        # Validações
        if item_dto.quantity <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        
        # Buscar item
        cart_item = self.cart_item_dao.get_by_id(item_id)
        if not cart_item or cart_item.cart.user_id != user_id:
            return None
        
        # Verificar disponibilidade do produto
        if not cart_item.product.is_available(item_dto.quantity):
            raise ValueError(f"Produto não disponível na quantidade solicitada. Estoque: {cart_item.product.stock}")
        
        return self.cart_item_dao.update_quantity(cart_item, item_dto.quantity)
    
    def remove_item_from_cart(self, user_id: int, item_id: int) -> bool:
        """Remove item do carrinho"""
        cart_item = self.cart_item_dao.get_by_id(item_id)
        if not cart_item or cart_item.cart.user_id != user_id:
            return False
        
        return self.cart_item_dao.delete(cart_item)
    
    def clear_user_cart(self, user_id: int) -> bool:
        """Limpa todos os itens do carrinho do usuário"""
        cart = self.cart_dao.get_by_user_id(user_id)
        if not cart:
            return False
        
        self.cart_dao.clear_cart(cart)
        return True
    
    def get_cart_dto(self, user_id: int) -> CartDTO:
        """Retorna DTO do carrinho"""
        cart = self.get_user_cart(user_id)
        return CartDTO.from_cart(cart)
    
    def validate_cart_for_purchase(self, user_id: int) -> tuple[bool, list[str]]:
        """Valida se o carrinho pode ser usado para compra"""
        cart = self.cart_dao.get_by_user_id(user_id)
        if not cart or not cart.items:
            return False, ["Carrinho vazio"]
        
        errors = []
        for item in cart.items:
            if not item.product.is_active:
                errors.append(f"Produto '{item.product.name}' não está mais disponível")
            elif not item.product.is_available(item.quantity):
                errors.append(f"Produto '{item.product.name}' não tem estoque suficiente. Disponível: {item.product.stock}")
        
        return len(errors) == 0, errors

