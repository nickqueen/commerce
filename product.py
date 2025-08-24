from src.models.user import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)
    image_url = db.Column(db.String(500))
    category = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    cart_items = db.relationship('CartItem', backref='product', lazy=True, cascade='all, delete-orphan')
    ticket_items = db.relationship('TicketItem', backref='product', lazy=True)

    def __repr__(self):
        return f'<Product {self.name}>'
    
    def is_available(self, quantity=1):
        """Verifica se o produto está disponível na quantidade solicitada"""
        return self.is_active and self.stock >= quantity
    
    def reduce_stock(self, quantity):
        """Reduz o estoque do produto"""
        if self.stock >= quantity:
            self.stock -= quantity
            return True
        return False
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'stock': self.stock,
            'image_url': self.image_url,
            'category': self.category,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

