from typing import List, Optional
from src.models.product import Product
from src.models.user import db

class ProductDAO:
    """Data Access Object para Product"""
    
    @staticmethod
    def create(product_data: dict) -> Product:
        """Cria um novo produto"""
        product = Product(**product_data)
        db.session.add(product)
        db.session.commit()
        return product
    
    @staticmethod
    def get_by_id(product_id: int) -> Optional[Product]:
        """Busca produto por ID"""
        return Product.query.get(product_id)
    
    @staticmethod
    def get_all() -> List[Product]:
        """Retorna todos os produtos"""
        return Product.query.all()
    
    @staticmethod
    def get_active_products() -> List[Product]:
        """Retorna apenas produtos ativos"""
        return Product.query.filter_by(is_active=True).all()
    
    @staticmethod
    def get_by_category(category: str) -> List[Product]:
        """Retorna produtos por categoria"""
        return Product.query.filter_by(category=category, is_active=True).all()
    
    @staticmethod
    def search_by_name(name: str) -> List[Product]:
        """Busca produtos por nome (busca parcial)"""
        return Product.query.filter(
            Product.name.ilike(f'%{name}%'),
            Product.is_active == True
        ).all()
    
    @staticmethod
    def get_available_products(min_stock: int = 1) -> List[Product]:
        """Retorna produtos disponíveis com estoque mínimo"""
        return Product.query.filter(
            Product.is_active == True,
            Product.stock >= min_stock
        ).all()
    
    @staticmethod
    def update(product: Product, update_data: dict) -> Product:
        """Atualiza um produto"""
        for key, value in update_data.items():
            if hasattr(product, key) and value is not None:
                setattr(product, key, value)
        db.session.commit()
        return product
    
    @staticmethod
    def delete(product: Product) -> bool:
        """Deleta um produto"""
        try:
            db.session.delete(product)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False
    
    @staticmethod
    def soft_delete(product: Product) -> Product:
        """Desativa um produto (soft delete)"""
        product.is_active = False
        db.session.commit()
        return product
    
    @staticmethod
    def update_stock(product: Product, new_stock: int) -> Product:
        """Atualiza o estoque de um produto"""
        product.stock = new_stock
        db.session.commit()
        return product
    
    @staticmethod
    def reduce_stock(product: Product, quantity: int) -> bool:
        """Reduz o estoque de um produto"""
        if product.stock >= quantity:
            product.stock -= quantity
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def increase_stock(product: Product, quantity: int) -> Product:
        """Aumenta o estoque de um produto"""
        product.stock += quantity
        db.session.commit()
        return product

