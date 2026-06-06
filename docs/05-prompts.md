# 05 — Prompts Utilizados na Construção

Registro cronológico dos prompts enviados ao [Cursor](https://cursor.com) durante o desenvolvimento deste projeto. O objetivo é documentar o fluxo de trabalho orientado por IA e servir de referência para reproduzir ou estender o projeto.

> **Contexto:** todo o código foi gerado pelo agente de IA, sem intervenção manual. Cada prompt abaixo representa uma instrução dada pelo desenvolvedor humano que orientou a próxima etapa.

---

## Índice rápido

| # | Tema | Resultado principal |
| - | ---- | ------------------- |
| 1 | Ideia inicial + stack | Sugestão de stack (FastAPI, React, PostgreSQL, Docker) |
| 2 | Documentação e planejamento | Pasta `docs/` com stack, planejamento, regras e etapas |
| 3–13 | Fases 1 a 10 | Execução incremental do roteiro em `docs/04-etapas-execucao.md` |
| 14 | Debug login + DataGrip | Correção de credenciais e banco `gerador_artigos` |
| 15 | Migração de IA | OpenAI → Gemini |
| 16 | Variáveis de ambiente | Atualização do `.env` para Gemini |
| 17 | WordPress (planejamento) | Decisão: mock agora, integração real depois |
| 18 | WordPress (implementação) | Porta + adapter mock + endpoint + UI |

---

## Prompts

### 1 — Ideia inicial e sugestão de stack

```
Quero criar um projeto novo que será um gerador de artigos para Wordpress utilizando IA.
Podemos utilizar a API da OpenIA para ser nossa LLM geradora de artigos.
Mas gostaria de uma sugestão de implementação de stack para backend e frontend, rodando cada um em um container, então vamos criar um docker compose.
Precisamos também de autenticação, e salvar os artigos criados por IA num banco de dados PostgreSQL, que está usando em um container.
Quero uma interface bem limpa e aplicando os princípios de UX design, utilizando o melhor pacote para configuração da interface, conforme a stack sugerida.
Qual stack você sugere?
```

**Desfecho:** definição da stack (FastAPI + React/Vite + Mantine + PostgreSQL + Docker Compose + JWT).

---

### 2 — Documentação e planejamento de trabalho

```
Está perfeito, quero gerar uma documentação disso, desde a sugestão dada das stacks, até este último que é o planejamento que vamos seguir, coloque tudo numa pasta na raiz do projeto com o nome "docs", não esquecer que temos regras para codificação a serem seguidas, estas rules, estão divididas entre o fornend (pasta rules/frontend) e backend (pasta reles/backend). Elabore um documento com as etapas a serem executadas, que iremos utilizar e atualizar a cada passo/fase executada.
```

**Desfecho:** criação de `docs/` com `01-stack.md`, `02-planejamento.md`, `03-regras-codificacao.md` e `04-etapas-execucao.md`.

---

### 3 — Fase 1

```
Iniciar a fase 1
```

**Desfecho:** infraestrutura Docker (`docker-compose.yml`, Dockerfiles, `.env.example`).

---

### 4 — PostgreSQL existente

```
Usar o container que já está rodando se precisar te passo o nome do usuário e senha, e precisamos definir o nome do banco para ser criado.
```

**Desfecho:** PostgreSQL externo ao Compose (container `db-postgres` no host); banco `gerador_artigos`; conexão via `host.docker.internal`.

---

### 5 — Fase 2

```
Seguir para Fase 2
```

**Desfecho:** backend fundacional (DDD, SQLAlchemy async, Alembic, `/health`, `/health/ready`).

---

### 6 — Fase 3

```
Seguir para a Fase 3
```

**Desfecho:** autenticação JWT com `fastapi-users` (registro, login, `/users/me`).

---

### 7 — Fase 4

```
Seguir para a Fase 4
```

**Desfecho:** artigos (CQRS, geração via LLM, CRUD, `/articles/generate`).

---

### 8 — Fase 5

```
Seguir para a Fase 5
```

**Desfecho:** scaffold frontend (Vite, React 19, Mantine, TanStack Query, Axios).

---

### 9 — Fase 6

```
Seguir para a Fase 6
```

**Desfecho:** feature `auth` (login, registro, sessão, rotas protegidas).

---

### 10 — Fase 7

```
Seguir para a Fase 7
```

**Desfecho:** feature `articles` (dashboard, geração com preview, edição).

---

### 11 — Fase 8

```
Seguir para a Fase 8
```

**Desfecho:** integração E2E (interceptor 401, `RequireGuest`, erros amigáveis, UX responsiva).

---

### 12 — Fase 9

```
Seguir para a Fase 9
```

**Desfecho:** testes automatizados (pytest + Vitest).

---

### 13 — Fase 10

```
Seguir para a Fase 10
```

**Desfecho:** `README.md` completo, `.env.example` revisado, documentação final do MVP.

---

### 14 — Correção login e DataGrip

```
Nos testes de uso, não estou conseguindo logar, apesar do cadastro ter dado como ok. E não estou conseguindo visualizar as tabelas através do DataGrip, aparece o banco mas não as tabelas. Os docker estão rodando.
```

**Desfecho:** diagnóstico de `LOGIN_BAD_CREDENTIALS`; orientação DataGrip para banco `gerador_artigos` (não `denny`/`postgres`); auto-login após cadastro.

---

### 15 — Migração OpenAI → Gemini

```
Vamos ajustar para usar a API do Gemini em nosso backend, e não o OpenIA, ajustar a documentação sobre o ajuste.
```

**Desfecho:** adapter `GeminiArticleGenerator`, variáveis `GEMINI_API_KEY`/`GEMINI_MODEL`, docs atualizados.

---

### 16 — Atualização do `.env`

```
O arquivo do .env não precisa ser modificado? Se sim modificar o mesmo.
```

**Desfecho:** substituição de `OPENAI_*` por `GEMINI_*` no `.env` local.

---

### 17 — WordPress (decisão de abordagem)

```
Para a integração com o Wordpress visando a publicação automática é necessário termos, neste momento um blog montado, ou podemos preparar para um ajuste futuro, conforme o a necessidade? E neste projeto apenas deixar preparado e mockado com mensagem de envio?
```

**Desfecho:** confirmação de que **não** é necessário blog agora; abordagem porta/adapter com mock e mensagem de envio simulado.

---

### 18 — WordPress (implementação mockada)

```
Implementar a integração com o wordpress, deixando neste momento tudo mockado para integração real futura, de forma descomplicada. Fazer os ajustes nos arquivos em docs, .env e .ev.example
```

**Desfecho:** `WordPressPublisher`, `MockWordPressPublisher`, `RestWordPressPublisher` (stub), endpoint `POST /articles/{id}/publish-wordpress`, botão na UI, variáveis `WORDPRESS_*` em `.env` e `.env.example`.

---

## Observações

- Os prompts das **fases 3 a 13** são curtos e delegam a execução ao roteiro já documentado em [04 — Etapas de Execução](./04-etapas-execucao.md).
- Após a Fase 10, o projeto recebeu **evoluções adicionais** (Gemini, WordPress mock) orientadas pelos prompts 14 a 18.
- Para retomar o desenvolvimento, use o histórico deste documento junto com [04 — Etapas de Execução](./04-etapas-execucao.md) e [03 — Regras de Codificação](./03-regras-codificacao.md).
