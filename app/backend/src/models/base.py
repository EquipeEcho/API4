from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column


class Base(MappedAsDataclass, DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
