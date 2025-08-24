from src.models.user import db
from datetime import datetime, timedelta
import secrets

class PasswordResetToken(db.Model):
    __tablename__ = 'password_reset_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<PasswordResetToken user_id={self.user_id} expires_at={self.expires_at}>'
    
    @staticmethod
    def generate_token():
        """Gera um token seguro para reset de senha"""
        return secrets.token_urlsafe(32)
    
    @classmethod
    def create_for_user(cls, user_id):
        """Cria um novo token de reset para o usuário"""
        # Invalidar tokens existentes
        existing_tokens = cls.query.filter_by(user_id=user_id, used=False).all()
        for token in existing_tokens:
            token.used = True
        
        # Criar novo token
        token = cls(
            user_id=user_id,
            token=cls.generate_token(),
            expires_at=datetime.utcnow() + timedelta(hours=1)  # Expira em 1 hora
        )
        db.session.add(token)
        return token
    
    def is_valid(self):
        """Verifica se o token é válido (não usado e não expirado)"""
        return not self.used and datetime.utcnow() < self.expires_at
    
    def mark_as_used(self):
        """Marca o token como usado"""
        self.used = True
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'token': self.token,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'used': self.used,
            'is_valid': self.is_valid(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

