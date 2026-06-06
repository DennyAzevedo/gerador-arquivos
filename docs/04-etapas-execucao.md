# 04 — Etapas de Execução

Roteiro de fases do projeto. **Este é um documento vivo**: a cada passo/fase concluído, atualize o status, marque os itens do checklist e registre uma entrada no histórico ao final.

## Legenda de status

- ⬜ Pendente
- 🟡 Em andamento
- ✅ Concluído
- ⛔ Bloqueado

## Painel de fases

| Fase | Descrição | Status |
| ---- | --------- | ------ |
| 0 | Documentação e fundação | ✅ Concluído |
| 1 | Infraestrutura (Docker Compose + Dockerfiles) | ✅ Concluído |
| 2 | Backend — fundação (config, DB, domínio, camadas) | ✅ Concluído |
| 3 | Backend — autenticação (JWT / fastapi-users) | ✅ Concluído |
| 4 | Backend — geração de artigos (OpenAI) e CRUD | ✅ Concluído |
| 5 | Frontend — fundação (Vite + Mantine + Router) | ✅ Concluído |
| 6 | Frontend — autenticação (login/registro) | ✅ Concluído |
| 7 | Frontend — geração e gestão de artigos | ✅ Concluído |
| 8 | Integração ponta a ponta e ajustes de UX | ✅ Concluído |
| 9 | Testes automatizados | ✅ Concluído |
| 10 | Documentação final e revisão | ✅ Concluído |

---

## Fase 0 — Documentação e fundação ✅

- [x] Definir stack ([01 — Stack](./01-stack.md))
- [x] Definir planejamento e arquitetura ([02 — Planejamento](./02-planejamento.md))
- [x] Consolidar regras de codificação ([03 — Regras](./03-regras-codificacao.md))
- [x] Criar este roteiro de execução
- [x] Atualizar o `README.md` da raiz com link para `docs/`

## Fase 1 — Infraestrutura ✅

> **Decisão importante:** o PostgreSQL **não** faz parte do `docker-compose.yml`. Reutilizamos o container `db-postgres` (PostgreSQL 18) já existente no host, publicado em `localhost:5432`. O backend o acessa via `host.docker.internal:5432`. Banco do projeto: **`gerador_artigos`** (usuário `denny`).

- [x] `docker-compose.yml` com serviços `backend` e `frontend` (db é externo)
- [x] Conectar backend ao Postgres existente via `host.docker.internal` (`extra_hosts: host-gateway`)
- [x] Criar o banco `gerador_artigos` no container existente
- [x] `.env.example` com todas as variáveis (sem segredos reais)
- [x] `.gitignore` já cobre `.env`, `node_modules`, `__pycache__`, `venv` (com `!.env.example`)
- [x] `backend/Dockerfile` e `frontend/Dockerfile`
- [x] Validar `docker compose config` (sintaxe OK)
- [x] Validar conectividade com o Postgres via `host.docker.internal` (`pg_isready` OK)
- [ ] Build/boot completo de `backend` e `frontend` — depende dos manifestos criados nas Fases 2 e 5

## Fase 2 — Backend: fundação ✅

- [x] Estrutura de pastas em camadas (`api`, `application`, `domain`, `infrastructure`)
- [x] `requirements.txt` e `pyproject.toml`
- [x] `core/config.py` (settings via env, com `pydantic-settings`)
- [x] `infrastructure/db/session.py` (engine async + sessão)
- [x] Modelos de domínio (`User`, `Article`) isolados do ORM (dataclasses puras)
- [x] Modelos ORM em `infrastructure/db/models` (User compatível com fastapi-users)
- [x] Alembic configurado (async) + migração inicial `0001` (tabelas `users` e `articles`)
- [x] Endpoints `/health` (liveness) e `/health/ready` (readiness com checagem de DB)
- [x] Build do backend, migração aplicada e boot validado conectando ao Postgres

> **Notas:** a `DATABASE_URL` precisou codificar o `@` da senha como `%40`. O backend usa layout `src/` com `PYTHONPATH=/app/src`. Validações: `/health` → `{"status":"ok"}` (200); `/health/ready` → `{"status":"ready","database":"connected"}` (200); tabelas `users`, `articles` e `alembic_version` confirmadas no banco.

## Fase 3 — Backend: autenticação ✅

- [x] Integração `fastapi-users` (registro, login JWT) — wiring em `infrastructure/auth`
- [x] Repositório de usuários: port `UserRepository` (domínio) + `SqlAlchemyUserRepository` (infra) + mapper ORM→domínio + provider de DI
- [x] DTOs Pydantic (`UserRead`, `UserCreate`, `UserUpdate`)
- [x] Endpoint `/users/me` (via `get_users_router`)
- [x] Proteção de rotas por token (`current_active_user`)
- [x] Validar fluxo de auth

> **Endpoints:** `POST /auth/register`, `POST /auth/jwt/login`, `GET /users/me`. Estratégia JWT (Bearer), expiração 3600s.
>
> **Validação:** registro → `201`; login → `access_token`; `GET /users/me` com token → `200`; sem token → `401`. Usuário de teste removido após a validação. O `UserRepository` é a interface de domínio que será consumida pelos casos de uso de artigos (Fase 4); a persistência de auth usa o adapter do `fastapi-users`.

## Fase 4 — Backend: artigos e OpenAI ✅

- [x] Adapter da OpenAI em `infrastructure/openai` (`OpenAIArticleGenerator`, JSON mode)
- [x] Porta `ArticleGenerator` na camada de aplicação (+ `ArticleGenerationInput`/`GeneratedArticle`)
- [x] Caso de uso de geração (`GenerateArticleUseCase`) — não persiste
- [x] Repositório de artigos: port `ArticleRepository` (domínio) + `SqlAlchemyArticleRepository` + mapper
- [x] Casos de uso CQRS: commands (create/update/delete) e queries (list/get), com checagem de propriedade
- [x] DTOs de artigo (`GenerateArticleRequest`, `ArticleCreateRequest`, `ArticleUpdateRequest`, `ArticleResponse`, etc.)
- [x] Endpoints `POST /articles/generate`, `POST/GET/PUT/DELETE /articles[...]`
- [x] Validar geração e CRUD

> **Tratamento de erros:** `ArticleNotFoundError` → handler global `404`; `ArticleGenerationError` → `502` (sem stack trace). Acesso a artigos sempre filtrado por `user_id` (não-proprietário recebe `404`).
>
> **Validação:** CREATE `201`, LIST `200`, GET `200`, UPDATE `200` (status `draft`→`published`, `updated_at` alterado), GET inexistente `404`, DELETE `204`, GET pós-delete `404`. `GENERATE` com chave placeholder retornou `502` limpo (com chave válida, gera o artigo). Dados de teste removidos.

## Fase 5 — Frontend: fundação ✅

- [x] Scaffold Vite + React + TypeScript (strict) — `tsconfig` com `strict`, `noUnusedLocals/Parameters`
- [x] Dependências instaladas: Mantine 9.3, TanStack Query 5, React Router 7, Axios 1, React 19, Vite 8
- [x] `main.tsx` com providers (`MantineProvider`, `QueryClientProvider`, `BrowserRouter`, `Notifications`)
- [x] `app/layout/MainLayout` com `AppShell` + `HomePage` + roteamento
- [x] Cliente HTTP em `shared/api/client.ts` (axios) com interceptor de token + `shared/lib/authStorage`
- [x] App validado rodando no container

> **Estrutura:** `src/app` (layout, pages, App/rotas), `src/features` (auth/articles — Fases 6/7), `src/shared` (api, lib). Versões resolvidas via npm (sem inventar). Validação: Vite ready, `GET /` 200, `/src/main.tsx` 200, `tsc --noEmit` sem erros, lints limpos.

## Fase 6 — Frontend: autenticação ✅

- [x] Feature `auth`: `domain/types`, `services/authService`, `hooks` (useLogin/useRegister), `context/AuthContext`, `components` e `pages`
- [x] Páginas de Login e Registro com validação (`@mantine/form`)
- [x] `AuthContext` (bootstrap via `/users/me`) + `RequireAuth` (rotas protegidas)
- [x] Estados de loading (botões/loader) e erro (`Alert` + `getApiErrorMessage`) tratados
- [x] Login/registro integrados ao backend validados

> **Fluxo:** `/login` e `/register` públicos; demais rotas sob `RequireAuth` (redireciona p/ `/login`). Token em `localStorage`, injetado pelo interceptor do axios. Logout no header do `AppShell`. **Validação:** typecheck strict OK, lints OK, CORS p/ `localhost:5173` OK, registro (201), login (token) e `/users/me` (200) confirmados com os mesmos contratos do `authService`. (A interação visual deve ser conferida no navegador.)

## Fase 7 — Frontend: artigos ✅

- [x] Feature `articles`: `domain/types`, `services/articleService`, hooks (queries + mutations), components e pages
- [x] Dashboard com lista de artigos (`ArticleCard` com status, editar/excluir + modal de confirmação)
- [x] Tela de geração (`GenerateArticleForm` → preview editável `ArticleForm` → salvar)
- [x] Página de edição (`EditArticlePage`) com `useArticle` + `useUpdateArticle`
- [x] Feedback via `@mantine/notifications` (salvar, atualizar, excluir, erros)
- [x] Estados de loading, vazio (CTA) e erro tratados

> **Rotas:** `/` (Dashboard), `/articles/generate`, `/articles/:articleId/edit` (todas sob `RequireAuth`). `HomePage` placeholder removida.
>
> **Validação:** typecheck strict OK, lints OK; CRUD validado com os contratos do frontend — CREATE `201`, LIST `200`, GET `200`, UPDATE `200`, DELETE `204`, GET pós-delete `404`. A geração real depende de `OPENAI_API_KEY` válida (com placeholder, o backend retorna `502` tratado). Interação visual a conferir no navegador.

## Fase 8 — Integração ponta a ponta ✅

- [x] Subir a stack completa (`docker compose up`) com backend + frontend + Postgres existente
- [x] Fluxo completo validado (API): registrar → logar → criar → listar → editar → excluir
- [x] Redirecionamentos de auth: `RequireAuth` (→ `/login` com `from`), `RequireGuest` (autenticado → `/`), logout → `/login`
- [x] Tratamento de 401: interceptor global no axios + `UnauthorizedListener` (logout + notificação)
- [x] Ajustes de UX/responsividade: cards auth fluidos, header responsivo, nav no layout, grupos com wrap
- [x] Erros consistentes: `getApiErrorMessage` ampliado (validação FastAPI, rede, 401/404/502, códigos conhecidos)
- [x] Evidências registradas no histórico

> **Geração real:** continua dependendo de `OPENAI_API_KEY` válida no `.env` (placeholder retorna `502` tratado). **Validação automatizada:** FE `200`, backend ready, E2E CRUD `201/200/200/204`, token inválido `401`, generate `502`. Conferir fluxo visual no navegador em `http://localhost:5173` após `docker compose up`.

## Fase 9 — Testes automatizados ✅

**Backend (pytest):**
- [x] Configurar `pytest` + `pytest-asyncio` + `httpx` (`requirements-dev.txt`)
- [x] `tests/unit/domain/` — entidades e `ArticleNotFoundError`
- [x] `tests/unit/application/` — casos de uso com repositório/gerador fake
- [x] `tests/integration/infrastructure/` — `SqlAlchemyArticleRepository` (Postgres `gerador_artigos_test`)
- [x] `tests/api/` — auth, articles CRUD, `/health`, generate (override/502)

**Frontend (Vitest + Testing Library):**
- [x] Configurar Vitest + `@testing-library/react` + jsdom
- [x] `tests/shared/lib/` — `getApiErrorMessage`, `authStorage`
- [x] `tests/features/auth/` — `LoginForm`, `RequireAuth`, `RequireGuest`
- [x] `tests/features/articles/` — `DashboardPage` (loading/vazio/erro)

**Critérios de aceite:**
- [x] Happy path + edge cases + falhas esperadas
- [x] Comandos documentados abaixo

### Como executar os testes

**Backend** (requer Postgres com banco `gerador_artigos_test`):

```bash
docker compose run --rm \
  -e DATABASE_URL="postgresql+asyncpg://USER:SENHA@host.docker.internal:5432/gerador_artigos_test" \
  backend sh -c "pip install -r requirements-dev.txt && pytest"
```

**Frontend:**

```bash
docker compose run --rm --no-deps frontend sh -c "npm install && npm run test"
```

> **Resultado:** backend **22 passed**; frontend **13 passed** (6 arquivos).

## Fase 10 — Documentação final ✅

- [x] Atualizar `README.md` com instruções completas (build, execução, testes, variáveis de ambiente, segurança)
- [x] Revisar documentos de `docs/` (stack, planejamento, regras, etapas)
- [x] Registrar roadmap futuro (WordPress, CI/CD, agendamento, preview Markdown)
- [x] Validar `.env.example` alinhado ao estado atual (comentários, JWT 32 chars, URL encoding, TEST_DATABASE_URL)

> **Entregável:** README operacional para subir, usar e testar o projeto do zero. Segredos permanecem fora do Git (`.env` ignorado; apenas `.env.example` versionado).

---

## Histórico de execução

Registre aqui cada avanço relevante (data, fase, resumo).

| Data | Fase | Resumo |
| ---- | ---- | ------ |
| 2026-06-05 | 0 | Criada a documentação inicial em `docs/` (stack, planejamento, regras e etapas). |
| 2026-06-05 | 1 | Infraestrutura criada: `docker-compose.yml` (backend + frontend), Dockerfiles e `.env.example`. PostgreSQL passou a ser o container existente `db-postgres` (banco `gerador_artigos`), acessado via `host.docker.internal`. Validados `compose config` e conectividade ao banco. |
| 2026-06-05 | 2 | Backend fundacional em camadas (DDD): config, sessão async, entidades de domínio puras, modelos ORM (`users`, `articles`), Alembic async com migração `0001` e endpoints `/health` e `/health/ready`. Imagem construída, migração aplicada e endpoints validados (DB conectado). |
| 2026-06-05 | 3 | Autenticação JWT com `fastapi-users`: wiring (user manager, auth backend, instance), DTOs, `UserRepository` (port + impl SQLAlchemy + mapper) e routers de auth/register/users. Fluxo validado: registro (201), login (token), `/users/me` com token (200) e sem token (401). |
| 2026-06-05 | 4 | Artigos (CQRS + OpenAI): porta `ArticleGenerator` + adapter OpenAI, `ArticleRepository` (port + impl + mapper), casos de uso de geração e CRUD com checagem de propriedade, DTOs e endpoints `/articles/*` e `/articles/generate`. Handlers de erro (404/502). CRUD validado ponta a ponta; `generate` com erro tratado (502). |
| 2026-06-05 | 5 | Frontend fundacional: scaffold Vite + React 19 + TS strict, Mantine 9, TanStack Query 5, React Router 7 e Axios. Providers em `main.tsx`, layout `AppShell`, `HomePage`, cliente HTTP com interceptor de token e `authStorage`. Container validado (Vite servindo, typecheck e lints OK). |
| 2026-06-05 | 6 | Frontend auth: feature `auth` completa (types, service, hooks de mutation, `AuthContext`, formulários com `@mantine/form`, páginas Login/Registro), rotas protegidas (`RequireAuth`) e logout no layout. Tratamento de loading/erro. Validados typecheck, lints, CORS e integração (registro 201, login token, /users/me 200). |
| 2026-06-06 | 7 | Frontend artigos: feature `articles` (service, hooks query/mutation, `ArticleCard`, `ArticleForm`, `GenerateArticleForm`), Dashboard com lista/ações, geração com preview editável e página de edição. Notificações e estados loading/vazio/erro. `HomePage` removida. Validados typecheck, lints e CRUD integrado (201/200/200/204/404). |
| 2026-06-06 | 8 | Integração E2E: stack completa validada; interceptor 401 global, `RequireGuest`, return URL no login, logout com redirect, erros amigáveis ampliados, UX responsiva no layout/auth. E2E API: register→CRUD→delete OK; 401 e 502 tratados. Fase 9 detalhada no planejamento. |
| 2026-06-06 | 9 | Testes automatizados: backend pytest (22 testes — unit/application/domain, integration repositório, API auth/articles/health) com banco `gerador_artigos_test`; frontend Vitest (13 testes — lib, auth, dashboard). Comandos documentados em `docs/04`. |
| 2026-06-06 | 10 | Documentação final: `README.md` reescrito (setup, execução, testes, segurança, roadmap); `.env.example` revisado; Fase 10 concluída. Projeto MVP entregue. |
