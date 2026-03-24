from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column, registry

table_registry = registry()


# mapeamento ORM para user
@mapped_as_dataclass(table_registry)
class User:
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[int] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
