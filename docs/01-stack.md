# 01 — Stack Tecnológica

Documento que registra a stack sugerida para o projeto e a justificativa de cada escolha.

## Visão geral

| Camada | Tecnologia escolhida |
| ------ | -------------------- |
| Frontend | React + TypeScript + Vite + **Mantine** + TanStack Query + React Router |
| Backend | Python + **FastAPI** + SQLAlchemy 2.0 (async) + Alembic + Pydantic |
| Autenticação | JWT (OAuth2 password flow) via `fastapi-users` |
| IA / Geração | Google Gemini API (`google-genai`) |
| Banco de dados | PostgreSQL (container existente no host, `localhost:5432`) |
| Infraestrutura | Docker Compose (serviços: `frontend`, `backend`) |

## Diagrama de arquitetura

```
   Docker Compose                              Host
┌──────────────┐      ┌──────────────┐      ┌──────────────────┐
│  frontend    │─────►│   backend    │─────►│  db-postgres     │
│ React+Vite   │ HTTP │   FastAPI    │ SQL  │  PostgreSQL 18   │
│ Mantine :5173│◄─────│   :8000      │◄─────│  localhost:5432  │
└──────────────┘      └──────┬───────┘      └──────────────────┘
                             │ HTTPS         (via host.docker.internal)
                             ▼
                        Gemini API
```

## Backend — Python + FastAPI

- **FastAPI**: framework assíncrono, ideal para chamadas com latência alta (Gemini), com documentação automática (Swagger/OpenAPI) e validação nativa via Pydantic.
- **SQLAlchemy 2.0 (async)** + **asyncpg**: ORM moderno com suporte assíncrono.
- **Alembic**: versionamento e migração de schema.
- **Pydantic / pydantic-settings**: DTOs e configuração via variáveis de ambiente.
- **fastapi-users**: autenticação completa (registro, login, JWT, hash de senha) integrada ao PostgreSQL.
- **google-genai**: SDK oficial do Google para a API Gemini (geração de artigos).
- **Uvicorn**: servidor ASGI.

## Frontend — React + TypeScript + Vite

- **Vite**: build e dev server rápidos e modernos (CRA está descontinuado).
- **TypeScript (strict)**: segurança de tipos, essencial para qualidade sem revisão manual.
- **Mantine**: biblioteca de UI escolhida — completa (formulários, notificações, modais, hooks), limpa por padrão e com boa acessibilidade, alinhada aos princípios de UX.
- **TanStack Query**: gerenciamento de server state, cache e estados de carregamento/erro.
- **React Router**: navegação e rotas protegidas.
- **Axios**: cliente HTTP com interceptors para o token JWT.

## Banco de dados — PostgreSQL

- Reutilizamos o container **`db-postgres`** (PostgreSQL 18) já existente no host, publicado em `localhost:5432` — não criamos um serviço de banco no Compose.
- Banco do projeto: **`gerador_artigos`** (usuário `denny`).
- O backend o acessa via `host.docker.internal:5432` (mapeado com `extra_hosts: host-gateway`).
- Inspeção via **DataGrip (JetBrains)** direto em `localhost:5432` — por isso não há Adminer/pgAdmin.

## Infraestrutura — Docker Compose

Dois serviços (o PostgreSQL é externo ao Compose):

- `backend`: FastAPI; conecta ao Postgres do host via `host.docker.internal`.
- `frontend`: React + Vite; aponta para o backend.

Variáveis sensíveis ficam em `.env` (não versionado), com um `.env.example` versionado como referência.

## Decisões registradas

- **UI**: Mantine (confirmado pelo usuário).
- **Banco**: reutilizar o container existente `db-postgres` (PostgreSQL 18) no host, em vez de um serviço novo no Compose. Banco do projeto: `gerador_artigos`.
- **Visualização do banco**: nenhuma ferramenta no Compose; uso externo do DataGrip.
- **Modelo Gemini**: configurável por variável de ambiente (padrão sugerido: `gemini-2.0-flash`).
- **Publicação no WordPress**: prevista como etapa futura (roadmap), fora do primeiro ciclo.

## WordPress — publicação automática

- Porta `WordPressPublisher` na camada application; adapters em `infrastructure/wordpress`.
- **`MockWordPressPublisher`** (padrão): simula envio e retorna URL/mensagem de sucesso — não exige blog montado.
- **`RestWordPressPublisher`**: publicação real via `POST /wp-json/wp/v2/posts` quando `WORDPRESS_MOCK=false`.
- Variáveis: `WORDPRESS_MOCK`, `WORDPRESS_URL`, `WORDPRESS_USERNAME`, `WORDPRESS_APP_PASSWORD`.
- Endpoint: `POST /articles/{id}/publish-wordpress`.
- Chave de aplicativo WordPress: Usuários → Perfil → Senhas de aplicativo.

## Migração OpenAI → Gemini

O projeto utilizava inicialmente a OpenAI (`infrastructure/openai`). A geração de artigos foi migrada para a **API Gemini** do Google:

- Adapter em `infrastructure/gemini` (`GeminiArticleGenerator`)
- Variáveis: `GEMINI_API_KEY` e `GEMINI_MODEL` (substituem `OPENAI_*`)
- Chave obtida em [Google AI Studio](https://aistudio.google.com/apikey)
