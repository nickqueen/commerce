from src.models.user import db
from datetime import datetime

class Cart(db.Model):
    __tablename__ = 'carts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    items = db.relationship('CartItem', backref='cart', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Cart user_id={self.user_id}>'
    
    def get_total(self):
        """Calcula o total do carrinho"""
        return sum(item.get_subtotal() for item in self.items)
    
    def get_item_count(self):
        """Retorna o número total de itens no carrinho"""
        return sum(item.quantity for item in self.items)
    
    def clear(self):
        """Limpa todos os itens do carrinho"""
        for item in self.items:
            db.session.delete(item)
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'items': [item.to_dict() for item in self.items],
            'total': float(self.get_total()),
            'item_count': self.get_item_count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Constraint para evitar duplicatas
    __table_args__ = (db.UniqueConstraint('cart_id', 'product_id', name='unique_cart_product'),)

    def __repr__(self):
        return f'<CartItem cart_id={self.cart_id} product_id={self.product_id} quantity={self.quantity}>'
    
    def get_subtotal(self):
        """Calcula o subtotal do item (preço * quantidade)"""
        return self.product.price * self.quantity
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'cart_id': self.cart_id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'subtotal': float(self.get_subtotal()),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

