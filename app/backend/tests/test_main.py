import os


def test_root_endpoint(client):
    """Testa o endpoint raiz."""
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to EchoCad Api."


def test_upload_file_success(client, cleanup_uploads, dwg_file):
    """Testa upload bem-sucedido de arquivo DWG."""
    file_name = "teste.dwg"
    
    response = client.post(
        "/upload",
        files={"file": (file_name, dwg_file, "text/plain")}
    )
    
    cleanup_uploads.append(f"uploads/{file_name}")

    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == file_name
    assert data["file_size"] > 0
    assert len(data["file_hash"]) == 64  # SHA-256
    assert data["status"] == "Arquivo salvo com sucesso"


def test_upload_file_formats(client, cleanup_uploads, pdf_file, dwf_file):
    """Testa upload de diferentes formatos suportados (PDF e DWF)."""
    test_files = [
        ("documento.pdf", pdf_file),
        ("drawing.dwf", dwf_file),
    ]
    
    for file_name, file_content in test_files:
        response = client.post(
            "/upload",
            files={"file": (file_name, file_content, "text/plain")}
        )
        cleanup_uploads.append(f"uploads/{file_name}")
        
        assert response.status_code == 200
        assert response.json()["filename"] == file_name
        assert response.json()["file_size"] > 0


def test_upload_invalid_format(client, invalid_file):
    """Testa rejeição de arquivo com extensão não permitida."""
    file_name = "documento.txt"

    response = client.post(
        "/upload",
        files={"file": (file_name, invalid_file, "text/plain")}
    )

    assert response.status_code == 415
    assert "Formato não suportado" in response.json()["detail"]


def test_upload_no_filename(client, dwg_file):
    """Testa rejeição de upload sem nome de arquivo."""
    response = client.post(
        "/upload",
        files={"file": ("", dwg_file, "text/plain")}
    )

    # FastAPI retorna 422 para validação inválida
    assert response.status_code == 422


def test_upload_file_without_extension(client, invalid_file):
    """Testa rejeição de arquivo sem extensão válida."""
    file_name = "arquivo"

    response = client.post(
        "/upload",
        files={"file": (file_name, invalid_file, "text/plain")}
    )

    assert response.status_code == 415


def test_upload_multiple_files(client, cleanup_uploads, dwg_file, pdf_file, dwf_file):
    """Testa upload de múltiplos arquivos em sequência."""
    files_to_upload = [
        ("projeto1.dwg", dwg_file),
        ("projeto2.pdf", pdf_file),
        ("desenho.dwf", dwf_file),
    ]
    
    for file_name, file_content in files_to_upload:
        response = client.post(
            "/upload",
            files={"file": (file_name, file_content, "text/plain")}
        )
        cleanup_uploads.append(f"uploads/{file_name}")
        
        assert response.status_code == 200
        assert response.json()["filename"] == file_name


def test_hash_consistency(client, cleanup_uploads, dwg_file):
    """Testa se o hash SHA-256 é consistente para o mesmo arquivo."""
    file_name = "teste_hash.dwg"

    # Primeiro upload
    response1 = client.post(
        "/upload",
        files={"file": (file_name, dwg_file, "text/plain")}
    )
    hash1 = response1.json()["file_hash"]
    cleanup_uploads.append(f"uploads/{file_name}")
    
    if os.path.exists(f"uploads/{file_name}"):
        os.remove(f"uploads/{file_name}")
    
    # Segundo upload com mesmo conteúdo
    response2 = client.post(
        "/upload",
        files={"file": (file_name, dwg_file, "text/plain")}
    )
    hash2 = response2.json()["file_hash"]
    cleanup_uploads.append(f"uploads/{file_name}")

    # Hashes devem ser iguais
    assert hash1 == hash2
