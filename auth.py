from flask import Blueprint, request, jsonify
from src.repository.user_repository import UserRepository
from src.dto.user_dto import UserCreateDTO, UserLoginDTO
from src.middleware.auth_middleware import auth_middleware, require_auth

auth_bp = Blueprint('auth', __name__)
user_repository = UserRepository()

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registra um novo usuário"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        if not data or not all(k in data for k in ('username', 'email', 'password')):
            return jsonify({'error': 'Username, email e password são obrigatórios'}), 400
        
        # Criar DTO
        user_dto = UserCreateDTO(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            role=data.get('role', 'user')
        )
        
        # Criar usuário
        user = user_repository.create_user(user_dto)
        
        # Gerar token
        token = auth_middleware.generate_token(user.id)
        
        # Retornar resposta
        return jsonify({
            'message': 'Usuário criado com sucesso',
            'token': token,
            'user': user_repository.get_current_user_dto(user).__dict__
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Autentica um usuário"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        if not data or not all(k in data for k in ('email', 'password')):
            return jsonify({'error': 'Email e password são obrigatórios'}), 400
        
        # Criar DTO
        login_dto = UserLoginDTO(
            email=data['email'],
            password=data['password']
        )
        
        # Autenticar usuário
        user = user_repository.authenticate_user(login_dto.email, login_dto.password)
        
        if not user:
            return jsonify({'error': 'Credenciais inválidas'}), 401
        
        # Gerar token
        token = auth_middleware.generate_token(user.id)
        
        # Retornar resposta
        return jsonify({
            'message': 'Login realizado com sucesso',
            'token': token,
            'user': user_repository.get_current_user_dto(user).__dict__
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/current', methods=['GET'])
@require_auth
def current():
    """Retorna informações do usuário atual (apenas dados não sensíveis)"""
    try:
        user = request.current_user
        user_dto = user_repository.get_current_user_dto(user)
        
        return jsonify({
            'user': user_dto.__dict__
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/logout', methods=['POST'])
@require_auth
def logout():
    """Logout do usuário (apenas retorna mensagem, token deve ser removido no frontend)"""
    return jsonify({'message': 'Logout realizado com sucesso'}), 200

