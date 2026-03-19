from fastapi import FastAPI
from routes.upload import router

app = FastAPI()


app.include_router(router)


@app.get('/')
async def root():
    return {"message": "Welcome to EchoCad Api."}
