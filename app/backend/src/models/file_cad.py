from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry, mapped_as_dataclass

table_registry = registry()

# table de registro de arquivos de upload
# será usado depois pra facilitar o acesso aos arquivos
@mapped_as_dataclass(table_registry)
class FileCad:
    __tablename__ = 'files_cad'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    filename: Mapped[str] = mapped_column(nullable=False)
    file_size: Mapped[int] = mapped_column(nullable=False) 
    file_hash: Mapped[str] = mapped_column(unique=True, nullable=False)
    upload_at: Mapped[datetime] = mapped_column(server_default=func.now(), init=False)