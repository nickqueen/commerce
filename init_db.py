#!/usr/bin/env python3
"""
Script para inicializar o banco de dados com dados de exemplo
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from src.main import app
from src.models.user import db
from src.repository.user_repository import UserRepository
from src.repository.product_repository import ProductRepository
from src.dto.user_dto import UserCreateDTO
from src.dto.product_dto import ProductCreateDTO

def init_database():
    """Inicializa o banco de dados com dados de exemplo"""
    
    with app.app_context():
        # Criar todas as tabelas
        db.create_all()
        
        user_repo = UserRepository()
        product_repo = ProductRepository()
        
        print("🚀 Inicializando banco de dados...")
        
        # Criar usuário administrador
        try:
            admin_dto = UserCreateDTO(
                username="admin",
                email="admin@ecommerce.com",
                password="admin123",
                role="admin"
            )
            admin_user = user_repo.create_user(admin_dto)
            print(f"✅ Usuário administrador criado: {admin_user.username}")
        except ValueError as e:
            print(f"⚠️  Usuário admin já existe: {e}")
        
        # Criar usuário comum
        try:
            user_dto = UserCreateDTO(
                username="usuario",
                email="usuario@ecommerce.com",
                password="user123",
                role="user"
            )
            regular_user = user_repo.create_user(user_dto)
            print(f"✅ Usuário comum criado: {regular_user.username}")
        except ValueError as e:
            print(f"⚠️  Usuário comum já existe: {e}")
        
        # Criar produtos de exemplo
        products_data = [
            {
                "name": "Smartphone Samsung Galaxy",
                "description": "Smartphone Android com 128GB de armazenamento",
                "price": 899.99,
                "stock": 50,
                "category": "Eletrônicos",
                "image_url": "https://example.com/smartphone.jpg"
            },
            {
                "name": "Notebook Dell Inspiron",
                "description": "Notebook para uso profissional com 8GB RAM e SSD 256GB",
                "price": 2499.99,
                "stock": 25,
                "category": "Informática",
                "image_url": "https://example.com/notebook.jpg"
            },
            {
                "name": "Fone de Ouvido Bluetooth",
                "description": "Fone sem fio com cancelamento de ruído",
                "price": 199.99,
                "stock": 100,
                "category": "Áudio",
                "image_url": "https://example.com/fone.jpg"
            },
            {
                "name": "Camiseta Básica",
                "description": "Camiseta 100% algodão, disponível em várias cores",
                "price": 29.99,
                "stock": 200,
                "category": "Roupas",
                "image_url": "https://example.com/camiseta.jpg"
            },
            {
                "name": "Livro de Programação",
                "description": "Guia completo para desenvolvimento web moderno",
                "price": 79.99,
                "stock": 75,
                "category": "Livros",
                "image_url": "https://example.com/livro.jpg"
            },
            {
                "name": "Mouse Gamer",
                "description": "Mouse óptico com 6 botões programáveis",
                "price": 149.99,
                "stock": 80,
                "category": "Informática",
                "image_url": "https://example.com/mouse.jpg"
            },
            {
                "name": "Cafeteira Elétrica",
                "description": "Cafeteira automática para 12 xícaras",
                "price": 299.99,
                "stock": 30,
                "category": "Eletrodomésticos",
                "image_url": "https://example.com/cafeteira.jpg"
            },
            {
                "name": "Tênis Esportivo",
                "description": "Tênis para corrida com tecnologia de amortecimento",
                "price": 249.99,
                "stock": 60,
                "category": "Calçados",
                "image_url": "https://example.com/tenis.jpg"
            }
        ]
        
        for product_data in products_data:
            try:
                product_dto = ProductCreateDTO(**product_data)
                product = product_repo.create_product(product_dto)
                print(f"✅ Produto criado: {product.name}")
            except Exception as e:
                print(f"⚠️  Erro ao criar produto {product_data['name']}: {e}")
        
        print("\n🎉 Banco de dados inicializado com sucesso!")
        print("\n📋 Credenciais de acesso:")
        print("👤 Administrador:")
        print("   Email: admin@ecommerce.com")
        print("   Senha: admin123")
        print("\n👤 Usuário comum:")
        print("   Email: usuario@ecommerce.com")
        print("   Senha: user123")
        print("\n🚀 Para iniciar o servidor, execute:")
        print("   cd ecommerce-server")
        print("   source venv/bin/activate")
        print("   python src/main.py")

if __name__ == "__main__":
    init_database()

