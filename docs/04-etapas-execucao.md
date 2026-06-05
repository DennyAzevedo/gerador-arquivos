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
| 0 | Documentação e fundação | 🟡 Em andamento |
| 1 | Infraestrutura (Docker Compose + Dockerfiles) | ⬜ Pendente |
| 2 | Backend — fundação (config, DB, domínio, camadas) | ⬜ Pendente |
| 3 | Backend — autenticação (JWT / fastapi-users) | ⬜ Pendente |
| 4 | Backend — geração de artigos (OpenAI) e CRUD | ⬜ Pendente |
| 5 | Frontend — fundação (Vite + Mantine + Router) | ⬜ Pendente |
| 6 | Frontend — autenticação (login/registro) | ⬜ Pendente |
| 7 | Frontend — geração e gestão de artigos | ⬜ Pendente |
| 8 | Integração ponta a ponta e ajustes de UX | ⬜ Pendente |
| 9 | Testes automatizados | ⬜ Pendente |
| 10 | Documentação final e revisão | ⬜ Pendente |

---

## Fase 0 — Documentação e fundação 🟡

- [x] Definir stack ([01 — Stack](./01-stack.md))
- [x] Definir planejamento e arquitetura ([02 — Planejamento](./02-planejamento.md))
- [x] Consolidar regras de codificação ([03 — Regras](./03-regras-codificacao.md))
- [x] Criar este roteiro de execução
- [x] Atualizar o `README.md` da raiz com link para `docs/`

## Fase 1 — Infraestrutura ⬜

- [ ] `docker-compose.yml` com serviços `db`, `backend`, `frontend`
- [ ] `db`: PostgreSQL 16, volume `pgdata`, porta `5432` exposta, healthcheck
- [ ] `.env.example` com todas as variáveis (sem segredos reais)
- [ ] Ajustar `.gitignore` (`.env`, artefatos de build, venv, node_modules)
- [ ] `backend/Dockerfile` e `frontend/Dockerfile`
- [ ] Validar `docker compose up` subindo os 3 containers

## Fase 2 — Backend: fundação ⬜

- [ ] Estrutura de pastas em camadas (`api`, `application`, `domain`, `infrastructure`)
- [ ] `requirements.txt` / `pyproject.toml`
- [ ] `core/config.py` (settings via env)
- [ ] `infrastructure/db/session.py` (engine async + sessão)
- [ ] Modelos de domínio (`User`, `Article`) isolados do ORM
- [ ] Modelos ORM em `infrastructure/db/models`
- [ ] Alembic configurado + migração inicial
- [ ] Endpoint `/health`
- [ ] Validar boot do backend conectando ao Postgres

## Fase 3 — Backend: autenticação ⬜

- [ ] Integração `fastapi-users` (registro, login JWT)
- [ ] Repositório de usuários (abstração + implementação)
- [ ] DTOs Pydantic (`UserRead`, `UserCreate`)
- [ ] Endpoint `/users/me`
- [ ] Proteção de rotas por token
- [ ] Validar fluxo de auth via `/docs`

## Fase 4 — Backend: artigos e OpenAI ⬜

- [ ] Adapter da OpenAI em `infrastructure/openai`
- [ ] Porta (interface) do gerador na camada de aplicação
- [ ] Caso de uso de geração (command) — não persiste
- [ ] Repositório de artigos (abstração + implementação)
- [ ] Casos de uso CRUD (commands/queries)
- [ ] DTOs de artigo (request/response)
- [ ] Endpoints `/articles/*` e `/articles/generate`
- [ ] Validar geração e CRUD via `/docs`

## Fase 5 — Frontend: fundação ⬜

- [ ] Scaffold Vite + React + TypeScript (strict)
- [ ] Instalar Mantine, TanStack Query, React Router, Axios
- [ ] `main.tsx` com providers (Mantine, Query, Router)
- [ ] `app/layout` com `AppShell`
- [ ] Cliente HTTP em `shared/api` com interceptor de token
- [ ] Validar app rodando no container

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
