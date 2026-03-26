from fastapi import FastAPI
from src.routes.upload import router

app = FastAPI()


app.include_router(router)


# rota de teste
@app.get('/')
async def root():
    """Rota de boas vindas, retorna uma mensagem
    indiciando que a api está online."""
    return {"message": "Welcome to EchoCad Api."}
