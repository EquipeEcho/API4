import shutil
from fastapi import APIRouter, UploadFile, File
from pathlib import Path

router = APIRouter(
    prefix='/upload',
    tags=['upload']
)

# definindo local de salvanmento dos arquivos
DEFAULT_PATH = Path('uploads')
DEFAULT_PATH.mkdir(parents=True, exist_ok=True)

@router.post('/')
async def upload(file: UploadFile = File()):
    file_path = DEFAULT_PATH.joinpath(file.filename)
    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "status": "salvo com sucesso."}
