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
    - Verifique se possui 300MB disponíveis para fazer a instalação do projeto

- **Node.js** (versão 18.x ou superior)
  - Download: https://nodejs.org/
  - Verifique a instalação: `node --version`

- **pnpm** (gerenciador de pacotes)
  - Instalação: `npm install -g pnpm`
  - Verifique a instalação: `pnpm --version`

- **Git**
  - Download: https://git-scm.com/downloads
  - Verifique a instalação: `git --version`

- **Python**
  - Download: https://www.python.org/downloads/
  - Verifique a instalação: `python --version`

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

## 📦 Instalação das Dependências

É recomendável criar um ambiente virtual, pois isso garante que bibliotecas e suas versões não entrem em conflito com outros projetos que você tenha.<br>
Por exemplo, imagine que você possui um projeto que apenas roda com uma versão mais antiga de Python, mas o EchoCAD utiliza a última versão disponível atualmente (04-2026), sem o ambiente virtual você não conseguirá rodar este outro projeto ao atualizar globalmente a versão do seu Python.

Para criar o ambiente virtual utilize o seguinte comando:

```bash
python -m venv venv
```

Inicie seu ambiente virtual com:
```bash
venv\Scripts\activate
```

E para sair do ambiente virtual escreva:
```bash
deactivate
```
>Lembre-se sempre de iniciar o ambiente virtual antes de executar o projeto

Na pasta `app`, execute:<br>
> Obs: Você terá que instalar as dependências tanto do frontend quanto do backend, mas ambos partem dessa mesma pasta `app`.

### Frontend

Navegue até a pasta do frontend com o seguinte comando:

```bash
cd frontend
```

Para instalar as dependências utilize o comando:
```bash
npm install
```

> Não feche o terminal ainda, você terá que abrir dois deles para rodar completamente o projeto

### Backend

Abra outro terminal para executar as seguintes funções, caso esteja usando o CMD você terá que abrir outro, mas com o VS Code basta clicar no sinal de `+` na direita no botão `TERMINAL` e `PORTS`.

A partir da pasta `app` navegue até a pasta do backend

```bash
cd backend
```

Instale as dependências com o comando:
```bash
pip install -r requirements.txt
```

---

## ▶️ Execução do Projeto

### Frontend

Primeiramente navegue até a pasta destinada para o frontend, caso esteja na pasta `app` digite o seguinte código:

```bash
# Na pasta app
cd frontend
```

Para executar o frontend, utilize o seguinte comando:
```bash
npm run dev
```

O retorno será principalmente uma lista com três links, apenas segure o `Ctrl` e clique no primeiro, ou seja, o Local.

### Backend

```bash
uvicorn src.main:app --reload
```

---

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