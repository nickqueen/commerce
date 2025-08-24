from functools import wraps
from flask import request, jsonify, current_app
import jwt
from src.repository.user_repository import UserRepository
from src.models.user import UserRole

class AuthMiddleware:
    """Middleware para autenticação e autorização"""
    
    def __init__(self):
        self.user_repository = UserRepository()
    
    def generate_token(self, user_id: int) -> str:
        """Gera um token JWT para o usuário"""
        payload = {
            'user_id': user_id,
            'exp': None  # Token sem expiração por simplicidade
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    def decode_token(self, token: str) -> dict:
        """Decodifica um token JWT"""
        try:
            return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.InvalidTokenError:
            return None
    
    def get_current_user(self):
        """Obtém o usuário atual a partir do token"""
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        payload = self.decode_token(token)
        
        if not payload:
            return None
        
        user = self.user_repository.get_user_by_id(payload['user_id'])
        if not user or not user.is_active:
            return None
        
        return user

# Instância global do middleware
auth_middleware = AuthMiddleware()

def require_auth(f):
    """Decorator que requer autenticação"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = auth_middleware.get_current_user()
        if not user:
            return jsonify({'error': 'Token de autenticação necessário'}), 401
        
        # Adicionar usuário ao contexto da requisição
        request.current_user = user
        return f(*args, **kwargs)
    
    return decorated_function

def require_admin(f):
    """Decorator que requer privilégios de administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = auth_middleware.get_current_user()
        if not user:
            return jsonify({'error': 'Token de autenticação necessário'}), 401
        
        if not user.is_admin():
            return jsonify({'error': 'Privilégios de administrador necessários'}), 403
        
        # Adicionar usuário ao contexto da requisição
        request.current_user = user
        return f(*args, **kwargs)
    
    return decorated_function

def require_user(f):
    """Decorator que requer que o usuário seja um usuário comum (não admin)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = auth_middleware.get_current_user()
        if not user:
            return jsonify({'error': 'Token de autenticação necessário'}), 401
        
        # Adicionar usuário ao contexto da requisição
        request.current_user = user
        return f(*args, **kwargs)
    
    return decorated_function

def optional_auth(f):
    """Decorator que permite autenticação opcional"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = auth_middleware.get_current_user()
        # Adicionar usuário ao contexto da requisição (pode ser None)
        request.current_user = user
        return f(*args, **kwargs)
    
    return decorated_function

