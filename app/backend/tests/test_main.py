from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_upload_file():
    # Cria um arquivo temporário em memória para o teste
    file_content = b"conteudo fake do arquivo"
    file_name = "teste.txt"

    response = client.post(
        "/upload",
        files={"file": (file_name, file_content, "text/plain")}
    )

    assert response.status_code == 200
    assert response.json()["filename"] == file_name
