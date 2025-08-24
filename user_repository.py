from typing import List, Optional
from src.dao.user_dao import UserDAO
from src.models.user import User, UserRole
from src.models.password_reset import PasswordResetToken
from src.dto.user_dto import UserCreateDTO, UserUpdateDTO, UserCurrentDTO, UserPublicDTO

class UserRepository:
    """Repository para operações de usuário usando o padrão Repository"""
    
    def __init__(self):
        self.dao = UserDAO()
    
    def create_user(self, user_dto: UserCreateDTO) -> User:
        """Cria um novo usuário"""
        # Validações
        if self.dao.email_exists(user_dto.email):
            raise ValueError("Email já está em uso")
        
        if self.dao.username_exists(user_dto.username):
            raise ValueError("Username já está em uso")
        
        # Preparar dados
        user_data = {
            'username': user_dto.username,
            'email': user_dto.email,
            'role': UserRole(user_dto.role) if user_dto.role else UserRole.USER
        }
        
        # Criar usuário
        user = User(**user_data)
        user.set_password(user_dto.password)  # Definir senha antes de salvar
        
        # Salvar no banco
        from src.models.user import db
        db.session.add(user)
        db.session.commit()
        
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Busca usuário por ID"""
        return self.dao.get_by_id(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Busca usuário por email"""
        return self.dao.get_by_email(email)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Busca usuário por username"""
        return self.dao.get_by_username(username)
    
    def get_all_users(self) -> List[User]:
        """Retorna todos os usuários"""
        return self.dao.get_all()
    
    def get_active_users(self) -> List[User]:
        """Retorna apenas usuários ativos"""
        return self.dao.get_active_users()
    
    def update_user(self, user_id: int, user_dto: UserUpdateDTO) -> Optional[User]:
        """Atualiza um usuário"""
        user = self.dao.get_by_id(user_id)
        if not user:
            return None
        
        # Validações
        if user_dto.email and self.dao.email_exists(user_dto.email, user_id):
            raise ValueError("Email já está em uso")
        
        if user_dto.username and self.dao.username_exists(user_dto.username, user_id):
            raise ValueError("Username já está em uso")
        
        # Preparar dados para atualização
        update_data = {}
        if user_dto.username:
            update_data['username'] = user_dto.username
        if user_dto.email:
            update_data['email'] = user_dto.email
        if user_dto.role:
            update_data['role'] = UserRole(user_dto.role)
        if user_dto.is_active is not None:
            update_data['is_active'] = user_dto.is_active
        
        return self.dao.update(user, update_data)
    
    def delete_user(self, user_id: int) -> bool:
        """Deleta um usuário"""
        user = self.dao.get_by_id(user_id)
        if not user:
            return False
        return self.dao.delete(user)
    
    def deactivate_user(self, user_id: int) -> Optional[User]:
        """Desativa um usuário (soft delete)"""
        user = self.dao.get_by_id(user_id)
        if not user:
            return None
        return self.dao.soft_delete(user)
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Autentica um usuário"""
        user = self.dao.get_by_email(email)
        if user and user.check_password(password) and user.is_active:
            return user
        return None
    
    def get_current_user_dto(self, user: User) -> UserCurrentDTO:
        """Retorna DTO seguro para rota /current"""
        return UserCurrentDTO.from_user(user)
    
    def get_public_user_dto(self, user: User) -> UserPublicDTO:
        """Retorna DTO público do usuário"""
        return UserPublicDTO.from_user(user)
    
    def request_password_reset(self, email: str) -> Optional[PasswordResetToken]:
        """Solicita reset de senha"""
        user = self.dao.get_by_email(email)
        if not user or not user.is_active:
            return None
        
        return self.dao.create_password_reset_token(user.id)
    
    def reset_password(self, token: str, new_password: str) -> bool:
        """Reseta a senha usando token"""
        reset_token = self.dao.get_valid_reset_token(token)
        if not reset_token:
            return False
        
        user = self.dao.get_by_id(reset_token.user_id)
        if not user:
            return False
        
        # Verificar se a nova senha é diferente da atual
        if user.check_password(new_password):
            raise ValueError("A nova senha deve ser diferente da senha atual")
        
        # Atualizar senha
        user.set_password(new_password)
        
        # Marcar token como usado
        self.dao.use_reset_token(reset_token)
        
        return True

