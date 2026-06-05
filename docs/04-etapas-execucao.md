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
| 6 | Frontend — autenticação (login/registro) | ⬜ Pendente |
| 7 | Frontend — geração e gestão de artigos | ⬜ Pendente |
| 8 | Integração ponta a ponta e ajustes de UX | ⬜ Pendente |
| 9 | Testes automatizados | ⬜ Pendente |
| 10 | Documentação final e revisão | ⬜ Pendente |

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

## Fase 6 — Frontend: autenticação ⬜

- [ ] Feature `auth` (domain, services, hooks, components, pages)
- [ ] Páginas de Login e Registro com validação (`@mantine/form`)
- [ ] Contexto/estado de autenticação + rotas protegidas
- [ ] Estados de loading e erro tratados
- [ ] Validar login/registro integrados ao backend

## Fase 7 — Frontend: artigos ⬜

- [ ] Feature `articles` (domain, services, hooks, components, pages)
- [ ] Dashboard com lista de artigos (cards, status, ações)
- [ ] Tela de geração (form → preview editável → salvar)
- [ ] Feedback via `@mantine/notifications`
- [ ] Estados de loading, vazio e erro

## Fase 8 — Integração ponta a ponta ⬜

- [ ] Fluxo completo: registrar → logar → gerar → editar → salvar → listar
- [ ] Ajustes de UX e responsividade
- [ ] Tratamento consistente de erros entre front e back

## Fase 9 — Testes automatizados ⬜

- [ ] Backend: testes unit (domínio/casos de uso) em `tests/unit`
- [ ] Backend: testes integration (repositórios/adapters) em `tests/integration`
- [ ] Backend: testes de API em `tests/api`
- [ ] Frontend: testes de hooks/validadores, componentes e fluxos em `tests/`
- [ ] Cobrir happy path, edge cases e falhas esperadas

## Fase 10 — Documentação final ⬜

- [ ] Atualizar `README.md` com instruções de build e execução
- [ ] Revisar todos os documentos de `docs/`
- [ ] Registrar próximos passos (ex.: publicação no WordPress)

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
