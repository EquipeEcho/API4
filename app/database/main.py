import chromadb

# Para salvar os dados em disco
client = chromadb.PersistentClient(path="./app/database/main_chromadb")

# Ou para rodar apenas em memória (limpa ao fechar o script)
# client = chromadb.Client()


# Criando uma collection pra manusear os dados
collection = client.create_collection(name="meus_documentos")

collection.add(
    documents=[
        "O backend foi desenvolvido em Python com FastAPI",
        "O frontend utiliza React e Tailwind CSS",
        "O deploy é feito via Docker no servidor local"
    ],
    metadatas=[{"modulo": "back"}, {"modulo": "front"}, {"modulo": "infra"}],
    ids=["id1", "id2", "id3"]
)

# fazendo a consulta

results = collection.query(
    query_texts=["Como o servidor é implantado?"],
    n_results=1 # Quantidade de resultados próximos
)

print(results["documents"])
# Saída provável: [['O deploy é feito via Docker no servidor local']]


# Histórico da conversa com llm pra produção desse código
# https://gemini.google.com/share/ed35ccd77cb8