from sqlalchemy.orm import Session
from src.models.file_cad import FileCad

def save_file_metadata(db: Session, filename: str, file_size: int, file_hash: str):
    new_file = FileCad(filename=filename, file_size=file_size, file_hash=file_hash)
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file
