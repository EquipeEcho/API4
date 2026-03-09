# 📖 Manual de Instalação - EchoCAD

## 📋 Sumário

- [Pré-requisitos](#pré-requisitos)
- [Instalação do Ambiente](#instalação-do-ambiente)
- [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
- [Configuração das Variáveis de Ambiente](#configuração-das-variáveis-de-ambiente)
- [Instalação das Dependências](#instalação-das-dependências)
- [Execução do Projeto](#execução-do-projeto)
- [Verificação da Instalação](#verificação-da-instalação)
- [Solução de Problemas](#solução-de-problemas)

---

## 🔧 Pré-requisitos

Antes de iniciar a instalação, certifique-se de ter os seguintes softwares instalados em seu sistema:

### Obrigatórios

- **Armazenamento**
    - Verifique se possui xGB disponíveis para fazer a instalação do projeto

- **Node.js** (versão 18.x ou superior)
  - Download: https://nodejs.org/
  - Verifique a instalação: `node --version`

- **pnpm** (gerenciador de pacotes)
  - Instalação: `npm install -g pnpm`
  - Verifique a instalação: `pnpm --version`

- **Git**
  - Download: https://git-scm.com/downloads
  - Verifique a instalação: `git --version`

### Opcionais (mas recomendados)

- **VS Code** (Editor de código)
  - Download: https://code.visualstudio.com/

---

## 🚀 Instalação do Ambiente

### 1. Clone o Repositório

Abra o prompt de comando (cmd) e navegue até a pasta em que deseja armazenar o projeto.

```bash
# utilize o comando "cd" + nome da pasta
cd EchoDOC

# Clona o projeto na pasta atual
git clone https://github.com/EquipeEcho/EchoCAD
```

### 2. Acesse a pasta principal da aplicação

```bash
cd app
```

---

## 🗄️ Configuração do Banco de Dados

A definir

---

## ⚙️ Configuração das Variáveis de Ambiente

1. **Crie o arquivo `.env` na pasta `app`**

```bash
# Na pasta app
touch .env
```

2. **Configure as variáveis de ambiente**

Copie o conteúdo abaixo e ajuste conforme sua configuração:

```env
A definir
```

---

## 📦 Instalação das Dependências

Na pasta `app`, execute:

```bash
# Instalar todas as dependências do projeto
pnpm install

# Isso pode levar alguns minutos na primeira vez
```

### Verificar Instalação das Dependências

```bash
# Listar dependências instaladas
pnpm list
```

---

## ▶️ Execução do Projeto

### Modo Desenvolvimento

```bash
# Na pasta app
pnpm dev
```

O servidor estará disponível em: **http://localhost:3000**

### Modo Produção

```bash
# Build da aplicação
pnpm build

# Executar em produção
pnpm start
```

### Scripts Úteis

```bash
# Executar linter
pnpm lint

# Executar testes
pnpm test

# Popular banco de dados com dados de teste
pnpm seed
```

---

## ✅ Verificação da Instalação

### 1. Verifique se o servidor está rodando

Abra o navegador e acesse: **http://localhost:3000**

Você deve ver a página inicial do EchoDoc.

### 2. Teste a conexão com o banco de dados

```bash
A definir
```

### 3. Verifique os logs do servidor

No terminal onde você executou `pnpm dev`, você deve ver:

```
✓ Ready in 2.5s
○ Compiling / ...
✓ Compiled / in 1.2s
```

### 4. Teste o diagnóstico básico

1. Acesse http://localhost:3000
2. Clique em "Iniciar Diagnóstico"
3. Responda o questionário simplificado
4. Verifique se o diagnóstico é gerado corretamente

---

## 🔧 Solução de Problemas

### ❌ Erro: "Module not found"

**Solução:**
```bash
# Limpe o cache e reinstale as dependências
rm -rf node_modules
rm pnpm-lock.yaml
pnpm install
```

### ❌ Erro: "Port 3000 is already in use"

**Solução:**
```bash
# Windows - Encontre e mate o processo na porta 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:3000 | xargs kill -9

# Ou execute em outra porta
PORT=3001 pnpm dev
```

---

## 📞 Suporte

Se você encontrar problemas durante a instalação:

1. Verifique os logs de erro no terminal
2. Consulte a [documentação oficial do Next.js](https://nextjs.org/docs)
3. Verifique as issues no GitHub do projeto
4. Entre em contato com a equipe de desenvolvimento

---

## 🎉 Instalação Concluída!

Se você chegou até aqui e todos os testes passaram, parabéns! 🚀

Seu ambiente está configurado e pronto para desenvolvimento.

Próximos passos:
- Leia o [Manual do Usuário]()
- Consulte a [Documentação da API]()
- Explore o código e contribua!

---

**Desenvolvido pela Equipe Echo - FATEC SJC 2026-1**