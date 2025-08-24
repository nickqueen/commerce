from dataclasses import dataclass
from typing import Optional

@dataclass
class ProductCreateDTO:
    """DTO para criação de produto"""
    name: str
    description: Optional[str]
    price: float
    stock: int
    image_url: Optional[str] = None
    category: Optional[str] = None

@dataclass
class ProductUpdateDTO:
    """DTO para atualização de produto"""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None

@dataclass
class ProductPublicDTO:
    """DTO para informações públicas do produto"""
    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int
    image_url: Optional[str]
    category: Optional[str]
    is_active: bool
    
    @classmethod
    def from_product(cls, product):
        """Cria DTO a partir do modelo Product"""
        return cls(
            id=product.id,
            name=product.name,
            description=product.description,
            price=float(product.price),
            stock=product.stock,
            image_url=product.image_url,
            category=product.category,
            is_active=product.is_active
        )

