import pytest
import hashlib
from src.models.file_cad import FileCad
from src.controller.file_controller import save_file_metadata


@pytest.mark.parametrize("name, content, size", [
    ("projeto.dwg", b"dados_binarios_complexos_123", 28),
    ("vazio.dxf", b"", 0),
    ("nome com espaços.dwg", b"teste", 5),
])
def test_save_file_metadata(test_db, f_name, content, f_size):
    f_name = f_name
    f_size = f_size
    b_content = content
    f_hash = hashlib.sha256(b_content).hexdigest()
    file = save_file_metadata(test_db, f_name, f_size, f_hash)
    file_on_database = test_db.query(FileCad).filter(
        file.file_hash == f_hash).first()

    assert file_on_database is not None, "O arquivo deveria estar salvo no banco de dados"
    assert file_on_database.file_hash == f_hash
    assert file_on_database.filename == f_name
    assert file_on_database.file_size == f_size
