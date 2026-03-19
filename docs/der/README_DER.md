# DIAGRAMA ENTIDADE RELACIONAMENTO
## Versão 1.0 - pendente de revisão

### 1. Entidade: Usuário

Responsável pelo acesso ao sistema e autoria dos projetos.
- id_usuario (PK): Identificador único.
- nome: Nome completo do usuário.
- email: Endereço de e-mail (Login).
- senha: Hash da senha para autenticação.

### 2. Entidade: Projeto

O agrupador principal de todos os arquivos e memoriais.
- id_projeto (PK): Identificador único.
- titulo_projeto: Nome da obra ou serviço.
- descricao_projeto: Detalhamento do escopo do projeto.
- data_hora_criacao: Timestamp de quando o projeto foi aberto.

### 3. Entidade: Arquivo_CAD
Metadados do arquivo técnico processado pelo Python.
- id_arquivo (PK): Identificador único.
- nome_arquivo: Nome original do arquivo (ex: planta_baixa.dxf).
- caminho_arquivo: Path ou URL onde o arquivo está armazenado no servidor.

### 4. Entidade: Memorial de Cálculo

O documento técnico final gerado pelo software.
- id_memorial (PK): Identificador único.
- titulo_memorial: Título do documento (ex: "Memorial de Dimensionamento de Vigas").
- descricao_memorial: Texto narrativo (gerado ou auxiliado pelo Ollama).

### 5. Entidade: Disciplina

Classificação técnica do memorial.
- nome_disciplina (PK/AK): Área da engenharia (Estrutural, Hidráulica, Elétrica, etc.).

### 6. Entidade: Cálculos

Representa cada etapa ou "passo" matemático dentro de um memorial.
- id_calculo (PK): Identificador único.
 - descricao_calculo: Explicação sobre o que está sendo calculado nesta etapa.

### 7. Entidade: Variável_Cálculo

A unidade atômica da informação (Inputs e Outputs).
- id_variavel (PK): Identificador único.
- nome_variavel: Nome técnico (ex: L, base, fck).
- tipo_variavel: Categoria (Entrada Manual, Extraída do CAD, Resultado).
- descricao_variavel: O que a variável representa.
- valor_variavel: O valor numérico final.
- unidade_variavel: Unidade de medida (m, cm, kN, MPa).

### 8. Entidade: Norma_Técnica

A base legal e técnica que sustenta o cálculo.
- cod_normal (PK): Código da norma (ex: NBR 6118:2014).
- titulo_norma: Nome descritivo da norma.
- descricao_norma: Resumo ou link para a norma.

### 9. Entidade: Revisão_Memorial

Controle de versionamento do documento.
- id_revisao (PK): Identificador único.
- numero_revisao: Contador da versão (0, 1, 2...).
- data_revisao: Data da modificação.
- descricao_revisao: O que foi alterado nesta versão.

### 10. Entidade: Status_Aprovação

Workflow do documento.
- status_aprovacao: Estado atual (Em Elaboração, Aprovado, Reprovado).
- responsavel_aprovacao: Nome de quem validou o status.

### 11. Entidade: Anexo

Arquivos complementares.
- id_anexo (PK): Identificador único.
- titulo_anexo: Nome do anexo.
- descricao_anexo: Detalhes sobre o conteúdo do anexo.