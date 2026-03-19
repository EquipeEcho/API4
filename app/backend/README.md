# CONFIGURAÇÕES E COMANDOS

## Para usar o gerenciador de projetos Poetry

- Instalar o `Poetry` no sistema e comandos úteis.
```bash
pip install pipx
pipx ensurepath
pipx install poetry
poetry install
poetry self add poetry-plugin-export
poetry export -f requirements.txt --output requirements.txt --without-hashes --without dev
```
- Docker
```bash
docker build -t api:test .
docker run -d -p 8000:80 api:test
```