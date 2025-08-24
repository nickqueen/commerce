from dataclasses import dataclass
from typing import Optional

@dataclass
class UserCreateDTO:
    """DTO para criação de usuário"""
    username: str
    email: str
    password: str
    role: Optional[str] = "user"

@dataclass
class UserUpdateDTO:
    """DTO para atualização de usuário"""
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

@dataclass
class UserLoginDTO:
    """DTO para login de usuário"""
    email: str
    password: str

@dataclass
class UserCurrentDTO:
    """DTO para rota /current - apenas informações não sensíveis"""
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    
    @classmethod
    def from_user(cls, user):
        """Cria DTO a partir do modelo User"""
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role.value,
            is_active=user.is_active
        )

@dataclass
class UserPublicDTO:
    """DTO para informações públicas do usuário"""
    id: int
    username: str
    
    @classmethod
    def from_user(cls, user):
        """Cria DTO a partir do modelo User"""
        return cls(
            id=user.id,
            username=user.username
        )

@dataclass
class PasswordResetRequestDTO:
    """DTO para solicitação de reset de senha"""
    email: str

@dataclass
class PasswordResetDTO:
    """DTO para reset de senha"""
    token: str
    new_password: str

