import shutil
from fastapi import FastAPI, UploadFile, File

app = FastAPI()


@app.post('/upload')
def upload_file(file: UploadFile = File(...)):
    file_path = f'{file.filename}'
    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "status": "salvo com sucesso."}
