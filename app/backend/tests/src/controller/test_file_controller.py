import hashlib
import pytest

from sqlalchemy import select
from src.controller.file_controller import save_file_metadata
from src.models.file_cad import FileCad

@pytest.mark.parametrize("f_name, content, f_size", [
    ("projeto.dwg", b"dados_binarios_complexos_123", 28),
    ("vazio.dxf", b"", 0),
    ("nome com espaços.dwg", b"teste", 5),
])
def test_save_file_metadata(test_db, f_name, content, f_size):
    # --- ARRANGE ---
    b_content = content
    f_hash = hashlib.sha256(b_content).hexdigest()
    
    # --- ACT ---
    # Assume-se que o controller faz o session.add()
    file = save_file_metadata(test_db, f_name, f_size, f_hash)
    
    # IMPORTANTE: Garante que os dados foram para o banco de teste (memória/temp)
    test_db.flush() 

    # --- ASSERT ---
    # Usando o novo padrão select e filtrando pela Classe
    stmt = select(FileCad).where(FileCad.file_hash == f_hash)
    file_on_database = test_db.scalars(stmt).first()

    assert file_on_database is not None, "O arquivo deveria estar salvo no banco de dados"
    assert file_on_database.file_hash == f_hash
    assert file_on_database.filename == f_name
    assert file_on_database.file_size == f_size