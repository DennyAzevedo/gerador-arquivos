# Gerador de Artigos para WordPress

Gerador de artigos com Inteligência Artificial para publicação em blog WordPress. O sistema utiliza a API da OpenAI para gerar conteúdo, oferece uma interface web para configuração e revisão, e integra-se ao WordPress para publicação dos artigos.

> **Nota sobre o desenvolvimento:** Este projeto é desenvolvido integralmente com o [Cursor](https://cursor.com) como ferramenta de codificação assistida por IA, **sem intervenção manual no código**. O objetivo é validar e demonstrar um fluxo de desenvolvimento orientado por agentes de IA.

## Documentação

A documentação completa do projeto está na pasta [`docs/`](docs/README.md):

- [01 — Stack Tecnológica](docs/01-stack.md)
- [02 — Planejamento e Arquitetura](docs/02-planejamento.md)
- [03 — Regras de Codificação](docs/03-regras-codificacao.md)
- [04 — Etapas de Execução](docs/04-etapas-execucao.md) (roteiro vivo, atualizado a cada fase)

## Visão Geral

O objetivo do projeto é automatizar a criação e publicação de artigos em um blog WordPress, reduzindo o esforço manual de produção de conteúdo. O fluxo geral é:

1. O usuário define o tema, palavras-chave e parâmetros do artigo na interface web.
2. O backend aciona a API da OpenAI para gerar o conteúdo do artigo.
3. O usuário pode revisar e ajustar os parâmetros antes da publicação.
4. O artigo é enviado para o WordPress via API REST.

## Arquitetura

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│  Frontend   │ ───► │   Backend    │ ───► │   OpenAI    │
│  (React.js) │      │   (Python)   │      │     API     │
└─────────────┘      └──────┬───────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  WordPress   │
                     │   REST API   │
                     └──────────────┘
```

## Tecnologias

| Camada        | Tecnologia                          |
| ------------- | ----------------------------------- |
| Frontend      | React.js                            |
| Backend       | Python                              |
| IA / Geração  | OpenAI API                          |
| Publicação    | WordPress REST API                  |
| Ferramenta    | Cursor (desenvolvimento via IA)     |

## Estrutura do Projeto

> A estrutura será detalhada conforme o projeto evolui.

```
gerador-arquivos/
├── frontend/   # Aplicação React.js (a ser criada)
├── backend/    # API e lógica em Python (a ser criada)
├── LICENSE
└── README.md
```

## Pré-requisitos

- Node.js (para o frontend React.js)
- Python 3.x (para o backend)
- Conta e chave de API da OpenAI
- Site WordPress com a API REST habilitada e credenciais de acesso

## Configuração

> Instruções detalhadas de instalação e configuração serão adicionadas conforme o backend e o frontend forem implementados.

As credenciais sensíveis (chave da OpenAI, credenciais do WordPress) deverão ser configuradas via variáveis de ambiente, nunca versionadas no repositório.

## Roadmap

- [ ] Definir estrutura inicial do backend (Python)
- [ ] Definir estrutura inicial do frontend (React.js)
- [ ] Integração com a API da OpenAI para geração de artigos
- [ ] Integração com a API REST do WordPress para publicação
- [ ] Interface de configuração de parâmetros do artigo
- [ ] Interface de revisão e edição antes da publicação
- [ ] Agendamento de publicações
- [ ] Documentação de instalação e uso

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
