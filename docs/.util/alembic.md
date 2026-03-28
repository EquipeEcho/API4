# Uso do Alembic

O Alembic funciona como um sistema de controle de versão (semelhante ao Git) voltado especificamente para o banco de dados, permitindo gerenciar a evolução do seu schema à medida que os modelos do SQLAlchemy mudam. Ele automatiza a criação de scripts de migração que aplicam alterações — como criar novas tabelas, adicionar colunas ou modificar índices — de forma incremental e segura, garantindo que diferentes ambientes (desenvolvimento, teste e produção) estejam sempre sincronizados com a estrutura de dados definida no seu código.

```bash
pip install alembic
alembic init alembic
```

No `alembic.ini`: Localize a linha `sqlalchemy.url` e insira a string de conexão do seu banco.

Exemplo:
`sqlalchemy.url = sqlite:///meu_banco.db ou postgresql://:pass@localhost/dbname`

No `alembic/env.py`: Para habilitar a autogeração de migrações (onde o Alembic compara seus modelos com o banco), você precisa importar o seu Base.metadata.
No arquivo `env.py`, localize a variável `target_metadata = None` e altere para:

```python
from meu_projeto.models import Base
target_metadata = Base.metadata
```

|Comando|Descrição|
|:--|:--|
|alembic history | Lista todas as versões de migração criadas.|
|alembic current | Mostra qual a versão atual aplicada no banco.
|alembic upgrade +1 | Sobe uma versão à frente.
|alembic downgrade -1 | Reverte a última migração aplicada.
|alembic check | Verifica se o banco está sincronizado com os modelos.