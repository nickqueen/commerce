from typing import List, Optional, Tuple
from src.dao.ticket_dao import TicketDAO, TicketItemDAO
from src.dao.cart_dao import CartDAO
from src.dao.product_dao import ProductDAO
from src.models.ticket import Ticket, TicketStatus
from src.models.user import db
from src.dto.ticket_dto import TicketDTO

class TicketRepository:
    """Repository para operações de ticket usando o padrão Repository"""
    
    def __init__(self):
        self.ticket_dao = TicketDAO()
        self.ticket_item_dao = TicketItemDAO()
        self.cart_dao = CartDAO()
        self.product_dao = ProductDAO()
    
    def create_ticket_from_cart(self, user_id: int) -> Tuple[Ticket, bool]:
        """
        Cria um ticket a partir do carrinho do usuário
        Retorna: (ticket, is_complete)
        """
        cart = self.cart_dao.get_by_user_id(user_id)
        if not cart or not cart.items:
            raise ValueError("Carrinho vazio")
        
        # Calcular total inicial
        total_amount = cart.get_total()
        
        # Criar ticket
        ticket = self.ticket_dao.create(user_id, total_amount)
        
        # Processar cada item do carrinho
        all_items_fulfilled = True
        actual_total = 0
        
        try:
            for cart_item in cart.items:
                product = cart_item.product
                
                # Verificar disponibilidade
                available_quantity = min(cart_item.quantity, product.stock)
                
                if available_quantity == 0:
                    # Produto sem estoque - criar item com quantidade 0
                    self.ticket_item_dao.create(
                        ticket.id,
                        product.id,
                        cart_item.quantity,
                        float(product.price)
                    )
                    all_items_fulfilled = False
                else:
                    # Criar item do ticket
                    ticket_item = self.ticket_item_dao.create(
                        ticket.id,
                        product.id,
                        cart_item.quantity,
                        float(product.price)
                    )
                    
                    # Atualizar quantidade atendida
                    self.ticket_item_dao.update_fulfilled_quantity(ticket_item, available_quantity)
                    
                    # Reduzir estoque
                    self.product_dao.reduce_stock(product, available_quantity)
                    
                    # Calcular total real
                    actual_total += float(product.price) * available_quantity
                    
                    # Verificar se foi completamente atendido
                    if available_quantity < cart_item.quantity:
                        all_items_fulfilled = False
            
            # Atualizar status e total do ticket
            if all_items_fulfilled:
                self.ticket_dao.update_status(ticket, TicketStatus.COMPLETED)
            else:
                self.ticket_dao.update_status(ticket, TicketStatus.PARTIAL)
            
            self.ticket_dao.update_total(ticket, actual_total)
            
            # Limpar carrinho após processamento bem-sucedido
            self.cart_dao.clear_cart(cart)
            
            db.session.commit()
            
            return ticket, all_items_fulfilled
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    def get_ticket_by_id(self, ticket_id: int) -> Optional[Ticket]:
        """Busca ticket por ID"""
        return self.ticket_dao.get_by_id(ticket_id)
    
    def get_user_tickets(self, user_id: int) -> List[Ticket]:
        """Busca todos os tickets de um usuário"""
        return self.ticket_dao.get_by_user_id(user_id)
    
    def get_all_tickets(self) -> List[Ticket]:
        """Retorna todos os tickets (apenas para admin)"""
        return self.ticket_dao.get_all()
    
    def get_tickets_by_status(self, status: TicketStatus) -> List[Ticket]:
        """Busca tickets por status"""
        return self.ticket_dao.get_by_status(status)
    
    def get_pending_tickets(self) -> List[Ticket]:
        """Retorna tickets pendentes"""
        return self.get_tickets_by_status(TicketStatus.PENDING)
    
    def get_completed_tickets(self) -> List[Ticket]:
        """Retorna tickets completos"""
        return self.get_tickets_by_status(TicketStatus.COMPLETED)
    
    def get_partial_tickets(self) -> List[Ticket]:
        """Retorna tickets parciais"""
        return self.get_tickets_by_status(TicketStatus.PARTIAL)
    
    def cancel_ticket(self, ticket_id: int) -> Optional[Ticket]:
        """Cancela um ticket e restaura o estoque"""
        ticket = self.ticket_dao.get_by_id(ticket_id)
        if not ticket or ticket.status == TicketStatus.CANCELLED:
            return None
        
        try:
            # Restaurar estoque dos itens atendidos
            for item in ticket.items:
                if item.quantity_fulfilled > 0:
                    self.product_dao.increase_stock(item.product, item.quantity_fulfilled)
            
            # Atualizar status
            self.ticket_dao.update_status(ticket, TicketStatus.CANCELLED)
            
            db.session.commit()
            return ticket
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    def get_ticket_dto(self, ticket: Ticket) -> TicketDTO:
        """Retorna DTO do ticket"""
        return TicketDTO.from_ticket(ticket)
    
    def get_purchase_summary(self, user_id: int) -> dict:
        """Retorna resumo de compras do usuário"""
        tickets = self.get_user_tickets(user_id)
        
        total_tickets = len(tickets)
        completed_tickets = len([t for t in tickets if t.status == TicketStatus.COMPLETED])
        partial_tickets = len([t for t in tickets if t.status == TicketStatus.PARTIAL])
        cancelled_tickets = len([t for t in tickets if t.status == TicketStatus.CANCELLED])
        
        total_spent = sum(float(t.total_amount) for t in tickets if t.status != TicketStatus.CANCELLED)
        
        return {
            'total_tickets': total_tickets,
            'completed_tickets': completed_tickets,
            'partial_tickets': partial_tickets,
            'cancelled_tickets': cancelled_tickets,
            'total_spent': total_spent
        }

