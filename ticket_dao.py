from typing import List, Optional
from src.models.ticket import Ticket, TicketItem, TicketStatus
from src.models.user import db

class TicketDAO:
    """Data Access Object para Ticket"""
    
    @staticmethod
    def create(user_id: int, total_amount: float) -> Ticket:
        """Cria um novo ticket"""
        ticket = Ticket(
            user_id=user_id,
            total_amount=total_amount,
            status=TicketStatus.PENDING
        )
        db.session.add(ticket)
        db.session.commit()
        return ticket
    
    @staticmethod
    def get_by_id(ticket_id: int) -> Optional[Ticket]:
        """Busca ticket por ID"""
        return Ticket.query.get(ticket_id)
    
    @staticmethod
    def get_by_user_id(user_id: int) -> List[Ticket]:
        """Busca todos os tickets de um usuário"""
        return Ticket.query.filter_by(user_id=user_id).order_by(Ticket.created_at.desc()).all()
    
    @staticmethod
    def get_all() -> List[Ticket]:
        """Retorna todos os tickets"""
        return Ticket.query.order_by(Ticket.created_at.desc()).all()
    
    @staticmethod
    def get_by_status(status: TicketStatus) -> List[Ticket]:
        """Busca tickets por status"""
        return Ticket.query.filter_by(status=status).order_by(Ticket.created_at.desc()).all()
    
    @staticmethod
    def update_status(ticket: Ticket, status: TicketStatus) -> Ticket:
        """Atualiza o status de um ticket"""
        ticket.status = status
        db.session.commit()
        return ticket
    
    @staticmethod
    def update_total(ticket: Ticket, total_amount: float) -> Ticket:
        """Atualiza o total de um ticket"""
        ticket.total_amount = total_amount
        db.session.commit()
        return ticket

class TicketItemDAO:
    """Data Access Object para TicketItem"""
    
    @staticmethod
    def create(ticket_id: int, product_id: int, quantity_requested: int, unit_price: float) -> TicketItem:
        """Cria um novo item de ticket"""
        ticket_item = TicketItem(
            ticket_id=ticket_id,
            product_id=product_id,
            quantity_requested=quantity_requested,
            quantity_fulfilled=0,
            unit_price=unit_price
        )
        db.session.add(ticket_item)
        db.session.commit()
        return ticket_item
    
    @staticmethod
    def get_by_id(item_id: int) -> Optional[TicketItem]:
        """Busca item de ticket por ID"""
        return TicketItem.query.get(item_id)
    
    @staticmethod
    def get_by_ticket_id(ticket_id: int) -> List[TicketItem]:
        """Busca todos os itens de um ticket"""
        return TicketItem.query.filter_by(ticket_id=ticket_id).all()
    
    @staticmethod
    def update_fulfilled_quantity(ticket_item: TicketItem, quantity_fulfilled: int) -> TicketItem:
        """Atualiza a quantidade atendida de um item"""
        ticket_item.quantity_fulfilled = quantity_fulfilled
        db.session.commit()
        return ticket_item
    
    @staticmethod
    def fulfill_partial(ticket_item: TicketItem, available_quantity: int) -> TicketItem:
        """Atende parcialmente um item baseado na disponibilidade"""
        fulfilled = min(ticket_item.quantity_requested, available_quantity)
        ticket_item.quantity_fulfilled = fulfilled
        db.session.commit()
        return ticket_item

