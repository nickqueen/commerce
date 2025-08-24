from dataclasses import dataclass
from typing import List

@dataclass
class TicketItemDTO:
    """DTO para item do ticket"""
    id: int
    product_id: int
    product_name: str
    quantity_requested: int
    quantity_fulfilled: int
    unit_price: float
    subtotal: float
    is_fully_fulfilled: bool
    
    @classmethod
    def from_ticket_item(cls, ticket_item):
        """Cria DTO a partir do modelo TicketItem"""
        return cls(
            id=ticket_item.id,
            product_id=ticket_item.product_id,
            product_name=ticket_item.product.name,
            quantity_requested=ticket_item.quantity_requested,
            quantity_fulfilled=ticket_item.quantity_fulfilled,
            unit_price=float(ticket_item.unit_price),
            subtotal=float(ticket_item.get_subtotal()),
            is_fully_fulfilled=ticket_item.is_fully_fulfilled()
        )

@dataclass
class TicketDTO:
    """DTO para ticket"""
    id: int
    user_id: int
    status: str
    total_amount: float
    items: List[TicketItemDTO]
    created_at: str
    
    @classmethod
    def from_ticket(cls, ticket):
        """Cria DTO a partir do modelo Ticket"""
        return cls(
            id=ticket.id,
            user_id=ticket.user_id,
            status=ticket.status.value,
            total_amount=float(ticket.total_amount),
            items=[TicketItemDTO.from_ticket_item(item) for item in ticket.items],
            created_at=ticket.created_at.isoformat() if ticket.created_at else None
        )

@dataclass
class PurchaseRequestDTO:
    """DTO para solicitação de compra"""
    # Pode ser vazio se for para comprar todo o carrinho
    # Ou pode conter itens específicos no futuro
    pass

