from typing import List, Optional
from src.dao.product_dao import ProductDAO
from src.models.product import Product
from src.dto.product_dto import ProductCreateDTO, ProductUpdateDTO, ProductPublicDTO

class ProductRepository:
    """Repository para operações de produto usando o padrão Repository"""
    
    def __init__(self):
        self.dao = ProductDAO()
    
    def create_product(self, product_dto: ProductCreateDTO) -> Product:
        """Cria um novo produto"""
        # Validações
        if product_dto.price <= 0:
            raise ValueError("Preço deve ser maior que zero")
        
        if product_dto.stock < 0:
            raise ValueError("Estoque não pode ser negativo")
        
        # Preparar dados
        product_data = {
            'name': product_dto.name,
            'description': product_dto.description,
            'price': product_dto.price,
            'stock': product_dto.stock,
            'image_url': product_dto.image_url,
            'category': product_dto.category
        }
        
        return self.dao.create(product_data)
    
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Busca produto por ID"""
        return self.dao.get_by_id(product_id)
    
    def get_all_products(self) -> List[Product]:
        """Retorna todos os produtos"""
        return self.dao.get_all()
    
    def get_active_products(self) -> List[Product]:
        """Retorna apenas produtos ativos"""
        return self.dao.get_active_products()
    
    def get_products_by_category(self, category: str) -> List[Product]:
        """Retorna produtos por categoria"""
        return self.dao.get_by_category(category)
    
    def search_products(self, name: str) -> List[Product]:
        """Busca produtos por nome"""
        return self.dao.search_by_name(name)
    
    def get_available_products(self, min_stock: int = 1) -> List[Product]:
        """Retorna produtos disponíveis"""
        return self.dao.get_available_products(min_stock)
    
    def update_product(self, product_id: int, product_dto: ProductUpdateDTO) -> Optional[Product]:
        """Atualiza um produto"""
        product = self.dao.get_by_id(product_id)
        if not product:
            return None
        
        # Validações
        if product_dto.price is not None and product_dto.price <= 0:
            raise ValueError("Preço deve ser maior que zero")
        
        if product_dto.stock is not None and product_dto.stock < 0:
            raise ValueError("Estoque não pode ser negativo")
        
        # Preparar dados para atualização
        update_data = {}
        if product_dto.name:
            update_data['name'] = product_dto.name
        if product_dto.description is not None:
            update_data['description'] = product_dto.description
        if product_dto.price is not None:
            update_data['price'] = product_dto.price
        if product_dto.stock is not None:
            update_data['stock'] = product_dto.stock
        if product_dto.image_url is not None:
            update_data['image_url'] = product_dto.image_url
        if product_dto.category is not None:
            update_data['category'] = product_dto.category
        if product_dto.is_active is not None:
            update_data['is_active'] = product_dto.is_active
        
        return self.dao.update(product, update_data)
    
    def delete_product(self, product_id: int) -> bool:
        """Deleta um produto"""
        product = self.dao.get_by_id(product_id)
        if not product:
            return False
        return self.dao.delete(product)
    
    def deactivate_product(self, product_id: int) -> Optional[Product]:
        """Desativa um produto (soft delete)"""
        product = self.dao.get_by_id(product_id)
        if not product:
            return None
        return self.dao.soft_delete(product)
    
    def update_stock(self, product_id: int, new_stock: int) -> Optional[Product]:
        """Atualiza o estoque de um produto"""
        if new_stock < 0:
            raise ValueError("Estoque não pode ser negativo")
        
        product = self.dao.get_by_id(product_id)
        if not product:
            return None
        
        return self.dao.update_stock(product, new_stock)
    
    def reduce_stock(self, product_id: int, quantity: int) -> bool:
        """Reduz o estoque de um produto"""
        if quantity <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        
        product = self.dao.get_by_id(product_id)
        if not product:
            return False
        
        return self.dao.reduce_stock(product, quantity)
    
    def increase_stock(self, product_id: int, quantity: int) -> Optional[Product]:
        """Aumenta o estoque de um produto"""
        if quantity <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        
        product = self.dao.get_by_id(product_id)
        if not product:
            return None
        
        return self.dao.increase_stock(product, quantity)
    
    def get_product_dto(self, product: Product) -> ProductPublicDTO:
        """Retorna DTO público do produto"""
        return ProductPublicDTO.from_product(product)
    
    def check_availability(self, product_id: int, quantity: int) -> bool:
        """Verifica se o produto está disponível na quantidade solicitada"""
        product = self.dao.get_by_id(product_id)
        if not product:
            return False
        
        return product.is_available(quantity)

