from fastapi import FastAPI
from src.routes.upload import router

app = FastAPI()


app.include_router(router)


# rota de teste
@app.get('/')
async def root():
    return {"message": "Welcome to EchoCad Api."}
