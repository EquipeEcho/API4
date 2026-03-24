CREATE DATABASE EchoCAD_SQL;
USE EchoCAD_SQL;

-- mapeado em orm (wesley)
CREATE TABLE Usuario (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Email VARCHAR(150) UNIQUE NOT NULL,
    Senha VARCHAR(255) NOT NULL
);

CREATE TABLE Projetos (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(150) NOT NULL,
    Data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    Descricao_projeto TEXT,
    idUsuario INT,
    FOREIGN KEY (idUsuario) REFERENCES Usuario(ID)
);

CREATE TABLE Comandos_IA (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Comando_original TEXT,
    Intencao_detectada VARCHAR(255),
    Parametros_extraidos JSON,
    Data DATETIME DEFAULT CURRENT_TIMESTAMP,
    idUsuario INT,
    idProjetos INT,
    FOREIGN KEY (idUsuario) REFERENCES Usuario(ID),
    FOREIGN KEY (idProjetos) REFERENCES Projetos(ID)
);

CREATE TABLE Documentos_gerados (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Tipo_documento VARCHAR(100),
    Caminho_arquivo VARCHAR(255),
    Data_geracao DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Especificacoes_Tecnicas (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    idDocumentos_gerados INT,
    Categoria_tecnica VARCHAR(100),
    Descricao TEXT,
    Materiais_previstos TEXT,
    Norma_referencia VARCHAR(150),
    Observacoes TEXT,
    FOREIGN KEY (idDocumentos_gerados) REFERENCES Documentos_gerados(ID)
);

CREATE TABLE Calculos (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Tipo VARCHAR(100),
    Entrada_json JSON,
    Resultado_json JSON,
    Regra_aplicada TEXT
);

CREATE TABLE Memoriais_Calculo (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    idDocumentos_gerados INT,
    idCalculos INT,
    Resultados TEXT,
    Norma_referencia VARCHAR(150),
    Observacoes TEXT,
    FOREIGN KEY (idDocumentos_gerados) REFERENCES Documentos_gerados(ID),
    FOREIGN KEY (idCalculos) REFERENCES Calculos(ID)
);

CREATE TABLE Elementos (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Layer VARCHAR(100),
    Geometria VARCHAR(100),
    Comprimento DECIMAL(10,2),
    Area DECIMAL(10,2),
    Categoria_tecnica_tipo VARCHAR(100)
);

CREATE TABLE Arquivos (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Caminho VARCHAR(255),
    Nome_arquivo VARCHAR(150),
    Tipo VARCHAR(50),
    idProjetos INT,
    idCalculos INT,
    idDocumentos_gerados INT,
    idElementos INT,
    FOREIGN KEY (idProjetos) REFERENCES Projetos(ID),
    FOREIGN KEY (idCalculos) REFERENCES Calculos(ID),
    FOREIGN KEY (idDocumentos_gerados) REFERENCES Documentos_gerados(ID),
    FOREIGN KEY (idElementos) REFERENCES Elementos(ID)
);

CREATE TABLE Coordenadas (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    idElementos INT,
    X DECIMAL(10,4),
    Y DECIMAL(10,4),
    Ordem INT,
    FOREIGN KEY (idElementos) REFERENCES Elementos(ID)
);

CREATE TABLE Processamento (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Status VARCHAR(50),
    Data_inicio DATETIME,
    Data_fim DATETIME,
    Log_erro TEXT,
    Versao_parser VARCHAR(50),
    idArquivos INT,
    FOREIGN KEY (idArquivos) REFERENCES Arquivos(id)
); 

INSERT INTO Usuario (Nome, Email, Senha)
VALUES ('admin', 'admin@echocad.com', 'admin123');