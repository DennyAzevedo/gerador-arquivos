# 02 — Planejamento e Arquitetura

Detalhamento da arquitetura, estrutura de pastas, modelo de dados e contratos de API. A estrutura segue as regras de codificação do projeto (ver [03 — Regras de Codificação](./03-regras-codificacao.md)), com **arquitetura em camadas (DDD)** e testes em pasta dedicada.

## 1. Objetivo e escopo

Aplicação web conteinerizada que permite a um usuário autenticado:

1. Gerar artigos via Gemini a partir de um tema/parâmetros.
2. Revisar e editar o conteúdo gerado.
3. Salvar os artigos no PostgreSQL.
4. (Futuro) Publicar no WordPress via REST API.

## 2. Princípios arquiteturais

- Arquitetura em camadas: **presentation → application → domain** e **infrastructure** implementa as abstrações.
- Domínio puro: sem dependência de frameworks, ORM ou SDKs externos.
- ORM (SQLAlchemy) isolado na camada de infraestrutura; mapeamento explícito entre modelos ORM e entidades de domínio.
- DTOs com Pydantic na camada de API; entidades de domínio nunca expostas diretamente.
- Padrão **Repository** para persistência e **Adapter** para o Gemini.
- Testes em pasta `tests` separada, espelhando a estrutura da fonte.

## 3. Estrutura de pastas

### 3.1 Backend (camadas DDD)

```
backend/
├── Dockerfile
├── requirements.txt
├── pyproject.toml
├── alembic.ini
├── migrations/                      # Alembic (versões de schema)
├── src/
│   └── app/
│       ├── main.py                  # cria app FastAPI, CORS, routers
│       ├── core/
│       │   └── config.py            # Settings via env (pydantic-settings)
│       ├── api/                     # PRESENTATION
│       │   ├── routes/              # endpoints finos (auth, articles, health)
│       │   ├── dependencies/        # injeção (sessão, usuário atual)
│       │   └── schemas/             # DTOs Pydantic (request/response)
│       ├── application/             # APPLICATION (casos de uso)
│       │   ├── articles/
│       │   │   ├── commands/        # escrita (gerar, criar, editar, excluir)
│       │   │   ├── queries/         # leitura (listar, detalhar)
│       │   │   └── ports/           # interfaces (repositórios, gateway Gemini)
│       │   └── auth/
│       ├── domain/                  # DOMAIN (puro)
│       │   ├── articles/            # entidades, value objects, contratos
│       │   └── users/
│       └── infrastructure/          # INFRASTRUCTURE
│           ├── db/
│           │   ├── models/          # modelos SQLAlchemy
│           │   ├── repositories/    # implementações dos repositórios
│           │   └── session.py       # engine async + sessão
│           ├── gemini/              # adapter do SDK do Gemini
│           └── auth/                # config fastapi-users / JWT
└── tests/
    ├── unit/                        # domínio, casos de uso, validadores, mappers
    ├── integration/                 # repositórios, banco, adapter Gemini
    └── api/                         # endpoints, contratos, erros
```

### 3.2 Frontend (organização por feature/domínio)

```
frontend/
├── Dockerfile
├── package.json
├── vite.config.ts
├── tsconfig.json
├── src/
│   ├── main.tsx                     # MantineProvider + QueryClient + Router
│   ├── app/
│   │   ├── router.tsx               # rotas + rotas protegidas
│   │   └── layout/                  # AppShell (header + navbar)
│   ├── features/
│   │   ├── auth/
│   │   │   ├── components/          # presentation
│   │   │   ├── hooks/               # application (orquestração de estado)
│   │   │   ├── services/            # infrastructure (HTTP)
│   │   │   ├── domain/              # tipos, validação, contratos
│   │   │   └── pages/               # Login, Register
│   │   └── articles/
│   │       ├── components/          # ArticleCard, ArticleForm, ArticlePreview
│   │       ├── hooks/               # useGenerateArticle, useArticles
│   │       ├── services/            # chamadas à API de artigos
│   │       ├── domain/              # modelos/contratos de artigo
│   │       └── pages/               # Dashboard, GenerateArticle
│   └── shared/
│       ├── ui/                      # componentes reutilizáveis
│       ├── api/                     # cliente axios + interceptor de token
│       └── lib/                     # utilitários
└── tests/
    └── features/                    # espelha src/features
```

## 4. Modelo de dados

### User (via fastapi-users)
- `id` (UUID, PK)
- `email` (único)
- `hashed_password`
- `is_active`, `is_superuser`, `is_verified`
- `created_at`

### Article
- `id` (UUID, PK)
- `title`
- `content` (texto longo)
- `topic` / `prompt` (tema solicitado)
- `keywords` (palavras-chave)
- `tone` (tom do texto)
- `status` (`draft` | `published`)
- `user_id` (FK → User)
- `created_at`, `updated_at`

## 5. Contratos de API

| Método | Rota | Descrição | Auth |
| ------ | ---- | --------- | ---- |
| POST | `/auth/register` | Cadastro de usuário | Não |
| POST | `/auth/jwt/login` | Login → retorna JWT | Não |
| GET | `/users/me` | Dados do usuário logado | Sim |
| POST | `/articles/generate` | Gera artigo via Gemini (não salva) | Sim |
| POST | `/articles` | Cria/salva artigo | Sim |
| GET | `/articles` | Lista artigos do usuário | Sim |
| GET | `/articles/{id}` | Detalha artigo | Sim |
| PUT | `/articles/{id}` | Edita artigo | Sim |
| DELETE | `/articles/{id}` | Remove artigo | Sim |
| GET | `/health` | Healthcheck do container | Não |

## 6. Fluxo de telas (UX)

1. **Login / Registro** — formulários limpos e validados (`@mantine/form`).
2. **Dashboard** — `AppShell` com navbar lateral; lista de artigos em cards, com status e ações (editar/excluir).
3. **Gerar artigo** — formulário (tema, palavras-chave, tom, tamanho) → "Gerar" → preview editável → "Salvar".

Princípios de UX aplicados: hierarquia visual clara, feedback imediato (loading/erro/sucesso via `@mantine/notifications`), formulários validados, layout responsivo e tema consistente.

## 7. Infraestrutura (Docker Compose)

O PostgreSQL **não** faz parte do Compose: reutilizamos o container `db-postgres` (PostgreSQL 18) já existente no host. O backend o acessa via `host.docker.internal:5432`.

```yaml
services:
  backend:   # build ./backend, porta 8000, extra_hosts host.docker.internal:host-gateway
  frontend:  # build ./frontend, porta 5173, aponta para backend
```

### Variáveis de ambiente (`.env.example`)

```
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_DB=gerador_artigos
DATABASE_URL=postgresql+asyncpg://seu_usuario:sua_senha@host.docker.internal:5432/gerador_artigos
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-2.0-flash
JWT_SECRET=troque-este-segredo
CORS_ORIGINS=http://localhost:5173
VITE_API_URL=http://localhost:8000
```

## 8. Decisões assumidas (reversíveis)

- Modelo do Gemini configurável por env (`GEMINI_MODEL`, padrão `gemini-2.0-flash`).
- UUID como PK de usuários e artigos.
- Geração **não** salva automaticamente — usuário revisa antes (melhor UX e controle de custo).
- Publicação no WordPress fica para fase futura.
