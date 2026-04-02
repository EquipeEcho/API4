import shutil
import hashlib
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from pathlib import Path
import logging

from sqlalchemy.orm import Session
from src.database import get_session

from src.modules.Memorial.generatorteste import run_integration

router = APIRouter(
    prefix='/upload',
    tags=['upload']
)

DEFAULT_PATH = Path('uploads')
DEFAULT_PATH.mkdir(parents=True, exist_ok=True)


@router.post('/')
async def upload(file: UploadFile = File(...), db: Session = Depends(get_session)):
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Filename is required'
        )
    
    if not file.filename.lower().endswith(('dwg', 'dwf', 'dxf')):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail='Formato não suportado. Use .dwg, .dwf ou .dxf'
        )
    
    try:
        file_path = DEFAULT_PATH.joinpath(file.filename)
        
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        hash_sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        file_hash = hash_sha256.hexdigest()
        
        file_size = file_path.stat().st_size

        basepath = Path("src/modules/Memorial")
        template_file = (basepath / "model_memorial.xlsx").resolve()

        output_file = (basepath / f"memorial_{Path(file.filename).stem}.xlsx").resolve()

        run_integration(
            dxf_file=str(file_path),
            template_file=str(template_file),
            output_file=str(output_file)
        )

        return {
            "filename": file.filename,
            "file_size": file_size,
            "file_hash": file_hash,
            "memorial_gerado": str(output_file),
            "status": "Processado com sucesso"
        }

    except Exception as e:
        logging.error(f"Erro no processamento: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Erro ao processar arquivo: {str(e)}'
        )