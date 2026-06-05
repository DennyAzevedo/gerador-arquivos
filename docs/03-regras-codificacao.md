# 03 — Regras de Codificação

Resumo das regras que orientam toda a geração de código. As regras completas estão em `.cursor/rules/`, divididas entre `frontend/` e `backend/`. **Toda** geração de código deve respeitá-las.

> Em caso de divergência, as regras originais em `.cursor/rules/` prevalecem sobre este resumo.

## Princípios gerais (frontend e backend)

- Clareza acima de esperteza; código simples, legível e manutenível.
- Baixo acoplamento e alta coesão; composição sobre herança.
- Sem TODOs, placeholders, implementações falsas ou fluxos incompletos.
- Nomes significativos; funções pequenas; evitar aninhamento profundo.
- Código autoexplicativo; comentários só para contexto/decisões não óbvias.
- Nunca expor segredos; configuração via variáveis de ambiente.

## Backend (`.cursor/rules/backend`)

### Arquitetura em camadas
- `presentation` (endpoints) → `application` (casos de uso) → `domain` (regras de negócio).
- `infrastructure` implementa as interfaces de application/domain.
- O **domínio não depende** de frameworks, ORM ou libs externas.

### DDD
- Entidades, Value Objects, Aggregates, Repositories (interfaces) e Domain Services.
- Modelar pelo domínio de negócio, não pelo banco. Evitar modelos anêmicos.

### CQRS
- Separar Commands (escrita) de Queries (leitura).
- Queries retornam projeções/DTOs otimizados para leitura.

### Camada de API
- Controllers/endpoints finos: validam entrada, chamam a aplicação, retornam HTTP.
- Sempre usar DTOs (Pydantic). Nunca expor entidades de domínio ou ORM.

### Persistência
- Repositórios como abstrações; ORM (SQLAlchemy) só na infraestrutura.
- Mapeamento explícito entre camadas.

### Padrões de projeto (uso deliberado)
- Repository, Unit of Work, Factory, Strategy, Adapter, Facade, etc. — apenas quando resolvem um problema real. Não super-engenheirar CRUDs simples.

### Python específico
- Type hints em tudo; seguir PEP8.
- FastAPI como framework; Pydantic para DTOs.
- Levantar exceções significativas; tratamento de erros centralizado.

### Erros, logs e segurança
- Não engolir exceções nem expor stack traces.
- Distinguir erros de negócio, validação e técnicos; respostas consistentes.
- Logs estruturados, sem dados sensíveis. Validar/sanitizar toda entrada.

## Frontend (`.cursor/rules/frontend`)

### Arquitetura
- Organizar por feature/domínio.
- Separar: presentation (componentes/views), application (casos de uso, coordenação de estado), domain (regras, entidades, contratos), infrastructure (HTTP, storage, serviços).
- Regras de negócio fora de componentes puramente apresentacionais.
- DTOs do backend não ditam a estrutura interna do frontend (usar mappers).

### React + TypeScript
- TypeScript em modo strict; componentes funcionais e pequenos.
- Tipar props explicitamente; handlers nomeados (`handleClick`, `handleSubmit`).
- Lógica complexa fora do render; hooks customizados focados.

### Estado e dados
- Manter estado o mais local possível.
- Distinguir UI state, form state, server state e domain/application state.
- Isolar chamadas HTTP em serviços/infra; contratos tipados.
- Tratar explicitamente estados de loading, vazio, sucesso e erro.

### Formulários e validação
- Formulários como cidadãos de primeira classe; validação explícita (preferir baseada em schema em forms médios/grandes).

### Acessibilidade e estilo
- HTML semântico primeiro; acessível por teclado; foco visível; ARIA só quando necessário.
- Estilo consistente com o padrão do projeto (Mantine).

## Testes (frontend e backend)

- Testar comportamento, não detalhes de implementação.
- **Localização (obrigatório)**: testes em pasta `tests` dedicada, **nunca** colocados junto ao código de produção.
- Estrutura de testes espelha a estrutura da fonte.
- Estrutura Arrange / Act / Assert; nomes descritivos.
- Cobrir happy path, edge cases e falhas esperadas.
- Backend: unit (domínio/casos de uso), integration (repositórios/banco/adapters), api (endpoints/contratos).
- Frontend: unit (lógica/hooks/validadores), component (render/interações/estados), integration (fluxos/API). Sempre testar estados de loading, vazio e erro.

## Commits (Conventional Commits)

- Tipos: `feat`, `fix`, `refactor`, `docs`, `test`, `style`, `chore`, `perf`, `build`, `ci`.
- Escopo opcional quando agrega clareza: `feat(auth): add login form validation`.
- Modo imperativo; sem ponto final no assunto; assunto conciso.
- Corpo quando ajudar a explicar o quê e o porquê; foco na intenção, não no ruído de implementação.
