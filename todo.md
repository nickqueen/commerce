## Tarefas

### Fase 1: Análise e planejamento da arquitetura
- [x] Entender a arquitetura atual (assumindo uma arquitetura básica de servidor)
- [x] Definir as modificações necessárias para cada requisito
- [x] Esboçar a estrutura de pastas e arquivos para as novas implementações

### Fase 2: Implementação do padrão Repository e DAO/DTO
- [x] Implementar o padrão Repository para as entidades principais (e.g., Usuário, Produto, Carrinho)
- [x] Criar DAOs (Data Access Objects) para cada entidade
- [x] Definir DTOs (Data Transfer Objects) para as rotas e operações relevantes (e.g., rota /current)

### Fase 3: Sistema de autenticação e autorização com middleware
- [x] Modificar a rota `/current` para retornar um DTO com informações não sensíveis
- [x] Desenvolver um middleware de autorização para restringir o acesso a endpoints (admin para criar/atualizar/excluir produtos, usuário para adicionar ao carrinho)

### Fase 4: Sistema de recuperação de senha com email
- [x] Implementar a lógica de geração e envio de tokens de recuperação de senha por e-mail
- [x] Criar a rota para redefinir a senha usando o token
- [x] Garantir que o link expire após uma hora
- [x] Impedir que o usuário use a mesma senha anterior

### Fase 5: Modelo Ticket e lógica de compra aprimorada
- [x] Criar o modelo de Ticket com os campos necessários
- [x] Implementar a lógica de compra que verifica estoque e gera tickets
- [x] Lidar com compras completas e incompletas de maneira eficiente

### Fase 6: Configuração de variáveis de ambiente e finalização
- [x] Configurar variáveis de ambiente para email, banco de dados, etc.
- [x] Criar arquivo .env de exemplo
- [x] Testar todas as funcionalidades
- [x] Preparar para deploy

### Fase 7: Entrega do projeto completo ao usuário
- [x] Criar documentação do projeto
- [x] Preparar repositório GitHub
- [x] Entregar projeto completo

