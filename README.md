# MedQuery: Chatbot com Arquitetura RAG para Consulta de Informações Oficiais sobre Medicamentos da ANVISA

> Assistente inteligente especializado em informações sobre medicamentos utilizando Retrieval-Augmented Generation (RAG)

O MedQuery é um chatbot web desenvolvido para responder perguntas sobre medicamentos, utilizando a técnica de Retrieval-Augmented Generation (RAG). Foi desenvolvido como Trabalho de Graduação (TG) universitário.

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Arquitetura](#arquitetura)
- [Tecnologias](#tecnologias)
- [Funcionalidades](#funcionalidades)
- [Instalação](#instalação)
- [Uso](#uso)
- [Limitações](#limitações)
- [Contribuição](#contribuição)

## 🎯 Sobre o Projeto

O MedQuery consiste em uma aplicação web completa com backend em **Python/FastAPI** e frontend em **Next.js/React**, projetada especificamente para o contexto brasileiro. O núcleo da aplicação é um pipeline RAG que utiliza dados oficiais da ANVISA sobre medicamentos (`DADOS_ABERTOS_MEDICAMENTOS.csv`) para responder perguntas dos usuários.

### Como Funciona

1. **Processamento de Dados:** As informações do arquivo `.csv` são processadas e seus embeddings são armazenados em um banco de dados vetorial **ChromaDB**
2. **Recuperação:** Quando um usuário faz uma pergunta, o sistema recupera os documentos mais relevantes (dados de medicamentos) do banco vetorial
3. **Geração:** A pergunta do usuário e os documentos recuperados são enviados para o modelo de linguagem **Perplexity AI** (`sonar-pro`), que gera uma resposta em linguagem natural baseada no contexto fornecido
4. **Orquestração:** Todo o pipeline é orquestrado usando o framework **LangChain**

### Requisitos Funcionais

| ID | Requisito | Descrição |
|----|-----------|----------|
| RF01 | Autenticação de Usuários | O sistema deve permitir registro e login de usuários com email e senha, utilizando JWT para autenticação |
| RF02 | Consulta de Medicamentos | O sistema deve responder perguntas sobre princípios ativos, classes terapêuticas e detentores de registro de medicamentos |
| RF03 | Pipeline RAG | O sistema deve implementar Retrieval-Augmented Generation para buscar informações relevantes no banco vetorial antes de gerar respostas |
| RF04 | Interface de Chat | O sistema deve fornecer uma interface web responsiva para interação em tempo real com o chatbot |
| RF05 | Processamento de CSV | O sistema deve processar o arquivo DADOS_ABERTOS_MEDICAMENTOS.csv e gerar embeddings para armazenamento vetorial |
| RF06 | Busca Semântica | O sistema deve realizar busca semântica no ChromaDB para recuperar documentos relevantes baseados na pergunta do usuário |
| RF07 | Renderização de Respostas | O sistema deve renderizar respostas em formato markdown com formatação adequada |
| RF08 | Restrições de Segurança | O sistema deve recusar fornecer conselhos médicos, prescrições ou diagnósticos |

### Requisitos Não-Funcionais

| ID | Categoria | Requisito | Descrição |
|----|-----------|-----------|----------|
| RNF01 | Desempenho | Tempo de Resposta | O sistema deve retornar respostas do chatbot em até 5 segundos para 95% das consultas |
| RNF02 | Segurança | Criptografia de Senhas | Senhas de usuários devem ser armazenadas com hash bcrypt |
| RNF03 | Segurança | Autenticação JWT | Tokens JWT devem expirar após período definido e serem validados em cada requisição protegida |
| RNF04 | Escalabilidade | Banco Vetorial | O ChromaDB deve suportar milhares de embeddings de medicamentos com busca eficiente |
| RNF05 | Usabilidade | Interface Responsiva | A interface deve ser responsiva e funcionar em dispositivos desktop, tablet e mobile |
| RNF06 | Manutenibilidade | Arquitetura Modular | O código deve seguir arquitetura modular com separação clara entre frontend, backend e pipeline RAG |
| RNF07 | Confiabilidade | Tratamento de Erros | O sistema deve tratar erros graciosamente e informar o usuário quando não houver informações disponíveis |
| RNF08 | Portabilidade | Containerização | O sistema deve ser containerizado com Docker para facilitar deployment |
| RNF09 | Compatibilidade | Idioma | O sistema deve operar exclusivamente em português brasileiro |
| RNF10 | Tecnologia | Stack Moderna | Backend em Python 3.12+ com FastAPI e frontend em Next.js 16 com React 19 |

## 🏗️ Arquitetura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Banco de      │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   Dados         │
│                 │    │                 │    │   (SQLite)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐    ┌─────────────────┐
                    │   Pipeline RAG  │◄──►│   ChromaDB      │
                    │   (LangChain)   │    │   (Vetorial)    │
                    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Perplexity AI  │
                    │   (sonar-pro)   │
                    └─────────────────┘
```

### Componentes da Arquitetura

#### Frontend (Next.js)
- **Framework:** Next.js 16 com React 19
- **Estilização:** Tailwind CSS
- **Funcionalidades:** 
  - Interface de chat responsiva
  - Sistema de autenticação
  - Páginas de login/registro
  - Renderização de markdown para respostas

#### Backend (FastAPI)
- **API REST:** Endpoints para chat e autenticação
- **Autenticação:** JWT com bcrypt para senhas
- **Banco de Dados:** SQLite para usuários
- **Pipeline RAG:** Integração com LangChain e ChromaDB

#### Banco de Dados Vetorial
- **ChromaDB:** Armazenamento de embeddings dos medicamentos
- **Embeddings:** Sentence Transformers para vetorização
- **Busca Semântica:** Recuperação de documentos relevantes

#### IA e Processamento
- **LLM:** Perplexity AI (modelo sonar-pro)
- **Framework:** LangChain para orquestração
- **Embeddings:** Hugging Face Sentence Transformers

## 🚀 Tecnologias

### Backend
- **Python 3.12+**
- **FastAPI** - Framework web moderno e rápido
- **LangChain** - Framework para aplicações com LLM
- **ChromaDB** - Banco de dados vetorial
- **Perplexity AI** - Modelo de linguagem
- **SQLite** - Banco de dados para usuários
- **JWT** - Autenticação
- **uv** - Gerenciador de dependências Python

### Frontend
- **Next.js 16** - Framework React
- **React 19** - Biblioteca de interface
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Framework de estilização
- **React Markdown** - Renderização de markdown

### DevOps
- **Docker** - Containerização
- **Ubuntu** - Sistema operacional base

## ✨ Funcionalidades

### O que o chatbot PODE responder:

- **Princípios Ativos:** "Qual o princípio ativo do Tylenol?"
- **Classe Terapêutica:** "Qual a classe terapêutica do Losartana?"
- **Detentor do Registro:** "Qual empresa detém o registro do Neosoro?"
- **Nome do Produto:** Perguntas gerais sobre medicamentos pelo nome
- **Informações Regulamentares:** Detalhes como número de registro e status

### ⚠️ LIMITAÇÕES IMPORTANTES:

O sistema foi projetado com restrições de segurança e **recusará**:

- **Fornecer Conselhos Médicos:** Não pode dar instruções sobre uso, dosagens ou planos de tratamento
- **Indicar ou Prescrever:** Não sugere, recomenda ou prescreve medicamentos
- **Diagnosticar Condições:** Não realiza qualquer tipo de diagnóstico
- **Informações Fora da Base:** Se a resposta não estiver no CSV, informará que não possui informações suficientes
- **Fazer Suposições:** Programado para não adivinhar ou fornecer informações não explícitas

## 🛠️ Instalação

### Pré-requisitos
- Python 3.12+
- Node.js 18+
- uv (gerenciador de dependências Python)
- Docker (opcional)

### Instalação Local

1. **Clone o repositório:**
```bash
git clone <repository-url>
cd chatbot-with-rag
```

2. **Configure o backend:**
```bash
# Instale dependências Python com uv
uv sync

# Configure variáveis de ambiente
cp .env.example .env
# Edite o .env com suas chaves de API
```

3. **Configure o frontend:**
```bash
cd frontend
npm install
npm run build
```

4. **Execute a aplicação:**
```bash
# Backend (porta 8000)
uv run uvicorn app.main:app --reload

# Frontend (porta 3000)
cd frontend && npm start
```

### Instalação com Docker

```bash
# Build da imagem
docker build -t medquery .

# Execute o container
docker run -p 3000:3000 -p 8000:8000 medquery
```

## 📖 Uso

1. Acesse `http://localhost:3000`
2. Crie uma conta ou faça login
3. Navegue para a página de chat
4. Faça perguntas sobre medicamentos em português
5. Receba respostas baseadas em dados oficiais

### Exemplos de Perguntas

- "Oi, com o que voce pode me ajudar?"
- "Qual o principio ativo do Ozempic? Para o que ele serve?"
- "Estou com dor de cabeca, qual medicamento devo tomar?"
- "Qual o princípio ativo da Dipirona?"
- "Quem é o fabricante do Rivotril?"
- "Qual a classe terapêutica do Omeprazol?"

## ⚠️ Aviso Legal

**IMPORTANTE:** O MedQuery fornece apenas informações regulamentares sobre medicamentos baseadas em dados oficiais da ANVISA. As respostas são geradas por IA e **NÃO SUBSTITUEM** a orientação de um profissional de saúde qualificado.

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto foi desenvolvido como Trabalho de Graduação e está disponível para fins educacionais.