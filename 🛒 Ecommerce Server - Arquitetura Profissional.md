# 🛒 Ecommerce Server - Arquitetura Profissional

Um servidor de ecommerce desenvolvido com Flask, implementando padrões de projeto modernos, sistema de autenticação robusto e lógica de negócio avançada.

## 🏗️ Arquitetura

Este projeto implementa uma arquitetura profissional baseada em camadas:

- **Controllers (Routes)**: Gerenciam as requisições HTTP
- **Services**: Lógica de negócio e orquestração
- **Repositories**: Padrão Repository para abstração de dados
- **DAOs**: Data Access Objects para operações de banco
- **DTOs**: Data Transfer Objects para transferência segura de dados
- **Models**: Modelos de dados com SQLAlchemy
- **Middleware**: Autenticação e autorização

## 🚀 Funcionalidades

### 🔐 Autenticação e Autorização
- Sistema de login/registro com JWT
- Middleware de autorização baseado em roles (admin/user)
- Rota `/current` com DTOs seguros (sem informações sensíveis)
- Sistema de recuperação de senha por email

### 🛍️ Gestão de Produtos
- CRUD completo de produtos (apenas admin)
- Busca por categoria e nome
- Controle de estoque
- Soft delete (desativação)

### 🛒 Carrinho de Compras
- Adicionar/remover/atualizar itens
- Validação de estoque em tempo real
- Cálculo automático de totais
- Limpeza de carrinho

### 🎫 Sistema de Tickets (Compras)
- Lógica de compra avançada
- Processamento de compras completas e parciais
- Controle de estoque automático
- Cancelamento com restauração de estoque
- Histórico de compras

### 📧 Sistema de Email
- Recuperação de senha por email
- Templates HTML responsivos
- Tokens com expiração (1 hora)
- Validação de senha anterior

## 🛠️ Tecnologias

- **Flask**: Framework web
- **SQLAlchemy**: ORM para banco de dados
- **SQLite**: Banco de dados (desenvolvimento)
- **JWT**: Autenticação via tokens
- **Flask-CORS**: Suporte a CORS
- **Python-dotenv**: Gerenciamento de variáveis de ambiente
- **SMTP**: Envio de emails

## 📦 Instalação

### Pré-requisitos
- Python 3.8+
- pip

### Passos

1. **Clone o repositório**
```bash
git clone <repository-url>
cd ecommerce-server
```

2. **Ative o ambiente virtual**
```bash
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. **Inicialize o banco de dados**
```bash
python init_db.py
```

6. **Execute o servidor**
```bash
python src/main.py
```

O servidor estará disponível em `http://localhost:5000`

## ⚙️ Configuração

### Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e configure:

```env
# Configurações do Flask
SECRET_KEY=your-secret-key-here
FLASK_ENV=development

# Configurações de Email (SMTP)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com

# URL Base da Aplicação
BASE_URL=http://localhost:5000
```

### Configuração de Email

Para habilitar o envio de emails de recuperação de senha:

1. Configure um email SMTP (Gmail recomendado)
2. Para Gmail, use uma "Senha de App" em vez da senha normal
3. Preencha as variáveis `SMTP_*` no arquivo `.env`

## 📚 API Endpoints

### Autenticação
- `POST /api/auth/register` - Registrar usuário
- `POST /api/auth/login` - Login
- `GET /api/auth/current` - Usuário atual (protegido)
- `POST /api/auth/logout` - Logout

### Recuperação de Senha
- `POST /api/auth/forgot-password` - Solicitar reset
- `POST /api/auth/reset-password` - Redefinir senha
- `POST /api/auth/validate-reset-token` - Validar token

### Produtos
- `GET /api/products` - Listar produtos
- `GET /api/products/{id}` - Buscar produto
- `POST /api/products` - Criar produto (admin)
- `PUT /api/products/{id}` - Atualizar produto (admin)
- `DELETE /api/products/{id}` - Deletar produto (admin)

### Carrinho
- `GET /api/cart` - Buscar carrinho (usuário)
- `POST /api/cart/items` - Adicionar item (usuário)
- `PUT /api/cart/items/{id}` - Atualizar item (usuário)
- `DELETE /api/cart/items/{id}` - Remover item (usuário)
- `DELETE /api/cart/clear` - Limpar carrinho (usuário)

### Tickets (Compras)
- `POST /api/purchase` - Realizar compra (usuário)
- `GET /api/tickets` - Listar tickets do usuário
- `GET /api/tickets/{id}` - Buscar ticket específico
- `PATCH /api/tickets/{id}/cancel` - Cancelar ticket
- `GET /api/purchase-summary` - Resumo de compras

### Administração
- `GET /api/admin/tickets` - Todos os tickets (admin)
- `GET /api/admin/statistics` - Estatísticas (admin)

## 🔒 Autenticação

### Headers Necessários

Para endpoints protegidos, inclua o header:
```
Authorization: Bearer <jwt-token>
```

### Roles de Usuário

- **admin**: Pode gerenciar produtos e visualizar todos os tickets
- **user**: Pode gerenciar carrinho e realizar compras

## 🎯 Exemplos de Uso

### Registro de Usuário
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "joao",
    "email": "joao@email.com",
    "password": "senha123"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@email.com",
    "password": "senha123"
  }'
```

### Adicionar Produto ao Carrinho
```bash
curl -X POST http://localhost:5000/api/cart/items \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "product_id": 1,
    "quantity": 2
  }'
```

### Realizar Compra
```bash
curl -X POST http://localhost:5000/api/purchase \
  -H "Authorization: Bearer <token>"
```

## 🧪 Dados de Teste

Após executar `python init_db.py`, você terá:

### Usuários
- **Admin**: admin@ecommerce.com / admin123
- **Usuário**: usuario@ecommerce.com / user123

### Produtos
- 8 produtos de exemplo em diferentes categorias
- Estoques variados para testar compras parciais

## 🏗️ Estrutura do Projeto

```
ecommerce-server/
├── src/
│   ├── dao/              # Data Access Objects
│   ├── dto/              # Data Transfer Objects
│   ├── middleware/       # Middleware de autenticação
│   ├── models/           # Modelos SQLAlchemy
│   ├── repository/       # Padrão Repository
│   ├── routes/           # Controllers (Blueprints)
│   ├── service/          # Serviços (email, etc.)
│   ├── static/           # Arquivos estáticos
│   └── main.py           # Aplicação principal
├── venv/                 # Ambiente virtual
├── .env                  # Variáveis de ambiente
├── .env.example          # Exemplo de configuração
├── init_db.py            # Script de inicialização
├── requirements.txt      # Dependências
└── README.md             # Documentação
```

## 🔄 Fluxo de Compra

1. **Usuário adiciona produtos ao carrinho**
2. **Sistema valida disponibilidade em tempo real**
3. **Usuário solicita compra via `/api/purchase`**
4. **Sistema cria ticket e processa cada item:**
   - Verifica estoque disponível
   - Reduz estoque conforme disponibilidade
   - Marca quantidade atendida vs solicitada
5. **Ticket é marcado como:**
   - `COMPLETED`: Todos os itens atendidos
   - `PARTIAL`: Alguns itens sem estoque suficiente
6. **Carrinho é limpo após processamento**

## 🛡️ Segurança

- Senhas hasheadas com Werkzeug
- Tokens JWT para autenticação
- Middleware de autorização por role
- DTOs para evitar exposição de dados sensíveis
- Validação de entrada em todas as rotas
- Tokens de reset com expiração

## 🚀 Deploy

Para deploy em produção:

1. Configure variáveis de ambiente adequadas
2. Use um banco de dados robusto (PostgreSQL)
3. Configure um servidor SMTP real
4. Use um servidor web (Gunicorn + Nginx)
5. Configure HTTPS

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

---

**Desenvolvido com ❤️ usando Flask e boas práticas de arquitetura de software**

