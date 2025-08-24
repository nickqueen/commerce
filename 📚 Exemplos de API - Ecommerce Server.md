# 📚 Exemplos de API - Ecommerce Server

Este documento contém exemplos práticos de como usar a API do servidor de ecommerce.

## 🔐 Autenticação

### 1. Registrar Usuário

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "joao",
    "email": "joao@email.com",
    "password": "senha123"
  }'
```

**Resposta:**
```json
{
  "message": "Usuário criado com sucesso",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 3,
    "username": "joao",
    "email": "joao@email.com",
    "role": "user",
    "is_active": true
  }
}
```

### 2. Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@email.com",
    "password": "senha123"
  }'
```

### 3. Usuário Atual

```bash
curl -X GET http://localhost:5000/api/auth/current \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## 🛍️ Produtos

### 1. Listar Produtos

```bash
curl -X GET http://localhost:5000/api/products
```

### 2. Buscar por Categoria

```bash
curl -X GET "http://localhost:5000/api/products?category=Eletrônicos"
```

### 3. Buscar por Nome

```bash
curl -X GET "http://localhost:5000/api/products?search=smartphone"
```

### 4. Criar Produto (Admin)

```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN_ADMIN" \
  -d '{
    "name": "Tablet Android",
    "description": "Tablet com tela de 10 polegadas",
    "price": 599.99,
    "stock": 30,
    "category": "Eletrônicos",
    "image_url": "https://example.com/tablet.jpg"
  }'
```

## 🛒 Carrinho

### 1. Ver Carrinho

```bash
curl -X GET http://localhost:5000/api/cart \
  -H "Authorization: Bearer SEU_TOKEN"
```

### 2. Adicionar Item

```bash
curl -X POST http://localhost:5000/api/cart/items \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -d '{
    "product_id": 1,
    "quantity": 2
  }'
```

### 3. Atualizar Quantidade

```bash
curl -X PUT http://localhost:5000/api/cart/items/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -d '{
    "quantity": 3
  }'
```

### 4. Remover Item

```bash
curl -X DELETE http://localhost:5000/api/cart/items/1 \
  -H "Authorization: Bearer SEU_TOKEN"
```

### 5. Limpar Carrinho

```bash
curl -X DELETE http://localhost:5000/api/cart/clear \
  -H "Authorization: Bearer SEU_TOKEN"
```

## 🎫 Compras (Tickets)

### 1. Realizar Compra

```bash
curl -X POST http://localhost:5000/api/purchase \
  -H "Authorization: Bearer SEU_TOKEN"
```

**Resposta (Compra Completa):**
```json
{
  "message": "Compra realizada com sucesso! Todos os itens foram processados.",
  "ticket": {
    "id": 1,
    "user_id": 3,
    "status": "completed",
    "total_amount": 1199.98,
    "items": [
      {
        "id": 1,
        "product_id": 1,
        "product_name": "Smartphone Samsung Galaxy",
        "quantity_requested": 2,
        "quantity_fulfilled": 2,
        "unit_price": 899.99,
        "subtotal": 1799.98,
        "is_fully_fulfilled": true
      }
    ],
    "created_at": "2024-01-15T10:30:00"
  },
  "is_complete": true
}
```

**Resposta (Compra Parcial):**
```json
{
  "message": "Compra parcialmente realizada. Alguns itens não tinham estoque suficiente.",
  "ticket": {
    "id": 2,
    "status": "partial",
    "items": [
      {
        "quantity_requested": 5,
        "quantity_fulfilled": 3,
        "is_fully_fulfilled": false
      }
    ]
  },
  "is_complete": false
}
```

### 2. Listar Tickets do Usuário

```bash
curl -X GET http://localhost:5000/api/tickets \
  -H "Authorization: Bearer SEU_TOKEN"
```

### 3. Filtrar por Status

```bash
curl -X GET "http://localhost:5000/api/tickets?status=completed" \
  -H "Authorization: Bearer SEU_TOKEN"
```

### 4. Ver Ticket Específico

```bash
curl -X GET http://localhost:5000/api/tickets/1 \
  -H "Authorization: Bearer SEU_TOKEN"
```

### 5. Cancelar Ticket

```bash
curl -X PATCH http://localhost:5000/api/tickets/1/cancel \
  -H "Authorization: Bearer SEU_TOKEN"
```

### 6. Resumo de Compras

```bash
curl -X GET http://localhost:5000/api/purchase-summary \
  -H "Authorization: Bearer SEU_TOKEN"
```

## 🔑 Recuperação de Senha

### 1. Solicitar Reset

```bash
curl -X POST http://localhost:5000/api/auth/forgot-password \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@email.com"
  }'
```

### 2. Validar Token

```bash
curl -X POST http://localhost:5000/api/auth/validate-reset-token \
  -H "Content-Type: application/json" \
  -d '{
    "token": "TOKEN_RECEBIDO_POR_EMAIL"
  }'
```

### 3. Redefinir Senha

```bash
curl -X POST http://localhost:5000/api/auth/reset-password \
  -H "Content-Type: application/json" \
  -d '{
    "token": "TOKEN_RECEBIDO_POR_EMAIL",
    "new_password": "nova_senha123"
  }'
```

## 👑 Rotas Administrativas

### 1. Listar Todos os Tickets

```bash
curl -X GET http://localhost:5000/api/admin/tickets \
  -H "Authorization: Bearer TOKEN_ADMIN"
```

### 2. Estatísticas

```bash
curl -X GET http://localhost:5000/api/admin/statistics \
  -H "Authorization: Bearer TOKEN_ADMIN"
```

**Resposta:**
```json
{
  "statistics": {
    "total_tickets": 15,
    "completed_tickets": 10,
    "partial_tickets": 3,
    "cancelled_tickets": 2,
    "pending_tickets": 0,
    "total_revenue": 12599.85,
    "completion_rate": 66.67
  }
}
```

## 🔄 Fluxo Completo de Compra

### Passo 1: Login
```bash
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@ecommerce.com", "password": "user123"}' \
  | jq -r '.token')
```

### Passo 2: Adicionar Produtos ao Carrinho
```bash
curl -X POST http://localhost:5000/api/cart/items \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"product_id": 1, "quantity": 1}'

curl -X POST http://localhost:5000/api/cart/items \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"product_id": 3, "quantity": 2}'
```

### Passo 3: Verificar Carrinho
```bash
curl -X GET http://localhost:5000/api/cart \
  -H "Authorization: Bearer $TOKEN"
```

### Passo 4: Validar Carrinho
```bash
curl -X GET http://localhost:5000/api/cart/validate \
  -H "Authorization: Bearer $TOKEN"
```

### Passo 5: Realizar Compra
```bash
curl -X POST http://localhost:5000/api/purchase \
  -H "Authorization: Bearer $TOKEN"
```

### Passo 6: Verificar Tickets
```bash
curl -X GET http://localhost:5000/api/tickets \
  -H "Authorization: Bearer $TOKEN"
```

## 🚨 Códigos de Status HTTP

- **200**: Sucesso
- **201**: Criado com sucesso
- **206**: Sucesso parcial (compra parcial)
- **400**: Erro de validação
- **401**: Não autenticado
- **403**: Sem permissão
- **404**: Não encontrado
- **500**: Erro interno do servidor

## 🔧 Headers Necessários

Para todas as rotas protegidas:
```
Authorization: Bearer SEU_JWT_TOKEN
Content-Type: application/json
```

## 📝 Notas Importantes

1. **Tokens JWT**: Não expiram por padrão (para desenvolvimento)
2. **Estoque**: Verificado em tempo real durante compras
3. **Carrinho**: Limpo automaticamente após compra bem-sucedida
4. **Roles**: `admin` pode gerenciar produtos, `user` pode comprar
5. **Email**: Configurar SMTP para recuperação de senha funcionar

