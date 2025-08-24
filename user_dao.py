from typing import List, Optional
from src.models.user import User, db
from src.models.password_reset import PasswordResetToken

class UserDAO:
    """Data Access Object para User"""
    
    @staticmethod
    def create(user_data: dict) -> User:
        """Cria um novo usuário"""
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        """Busca usuário por ID"""
        return User.query.get(user_id)
    
    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        """Busca usuário por email"""
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        """Busca usuário por username"""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_all() -> List[User]:
        """Retorna todos os usuários"""
        return User.query.all()
    
    @staticmethod
    def get_active_users() -> List[User]:
        """Retorna apenas usuários ativos"""
        return User.query.filter_by(is_active=True).all()
    
    @staticmethod
    def update(user: User, update_data: dict) -> User:
        """Atualiza um usuário"""
        for key, value in update_data.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        db.session.commit()
        return user
    
    @staticmethod
    def delete(user: User) -> bool:
        """Deleta um usuário"""
        try:
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False
    
    @staticmethod
    def soft_delete(user: User) -> User:
        """Desativa um usuário (soft delete)"""
        user.is_active = False
        db.session.commit()
        return user
    
    @staticmethod
    def email_exists(email: str, exclude_user_id: Optional[int] = None) -> bool:
        """Verifica se email já existe"""
        query = User.query.filter_by(email=email)
        if exclude_user_id:
            query = query.filter(User.id != exclude_user_id)
        return query.first() is not None
    
    @staticmethod
    def username_exists(username: str, exclude_user_id: Optional[int] = None) -> bool:
        """Verifica se username já existe"""
        query = User.query.filter_by(username=username)
        if exclude_user_id:
            query = query.filter(User.id != exclude_user_id)
        return query.first() is not None
    
    @staticmethod
    def create_password_reset_token(user_id: int) -> PasswordResetToken:
        """Cria um token de reset de senha para o usuário"""
        token = PasswordResetToken.create_for_user(user_id)
        db.session.commit()
        return token
    
    @staticmethod
    def get_valid_reset_token(token: str) -> Optional[PasswordResetToken]:
        """Busca um token de reset válido"""
        reset_token = PasswordResetToken.query.filter_by(token=token).first()
        if reset_token and reset_token.is_valid():
            return reset_token
        return None
    
    @staticmethod
    def use_reset_token(token: PasswordResetToken) -> None:
        """Marca um token de reset como usado"""
        token.mark_as_used()
        db.session.commit()

