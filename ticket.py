from src.models.user import db
from datetime import datetime
import enum

class TicketStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    PARTIAL = "partial"
    CANCELLED = "cancelled"

class Ticket(db.Model):
    __tablename__ = 'tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Enum(TicketStatus), default=TicketStatus.PENDING, nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    items = db.relationship('TicketItem', backref='ticket', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Ticket {self.id} user_id={self.user_id} status={self.status.value}>'
    
    def calculate_total(self):
        """Calcula o total do ticket baseado nos itens"""
        return sum(item.get_subtotal() for item in self.items)
    
    def is_completed(self):
        """Verifica se o ticket foi completamente processado"""
        return self.status == TicketStatus.COMPLETED
    
    def is_partial(self):
        """Verifica se o ticket foi parcialmente processado"""
        return self.status == TicketStatus.PARTIAL
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status.value,
            'total_amount': float(self.total_amount),
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class TicketItem(db.Model):
    __tablename__ = 'ticket_items'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity_requested = db.Column(db.Integer, nullable=False)
    quantity_fulfilled = db.Column(db.Integer, default=0, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)  # Preço no momento da compra
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<TicketItem ticket_id={self.ticket_id} product_id={self.product_id} qty={self.quantity_fulfilled}/{self.quantity_requested}>'
    
    def get_subtotal(self):
        """Calcula o subtotal baseado na quantidade atendida"""
        return self.unit_price * self.quantity_fulfilled
    
    def is_fully_fulfilled(self):
        """Verifica se o item foi completamente atendido"""
        return self.quantity_fulfilled == self.quantity_requested
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'ticket_id': self.ticket_id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'quantity_requested': self.quantity_requested,
            'quantity_fulfilled': self.quantity_fulfilled,
            'unit_price': float(self.unit_price),
            'subtotal': float(self.get_subtotal()),
            'is_fully_fulfilled': self.is_fully_fulfilled(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

