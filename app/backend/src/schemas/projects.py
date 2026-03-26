from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    """Classe de validação da criação do modelo via POST"""
    id_usuario: int = Field(..., description='ID do usuário criador')
    name: str = Field(
        ...,
        min_length=1,
        max_length=150,
        description='Nome do projeto'
    )
    description: str | None = Field(
        None, description='Descrição opcional do projeto')


class ProjectPublic(ProjectCreate):
    """Classe para consulta do usuário via GET"""
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        ...,
        description='ID gerado automaticamente pelo banco'
    )
    created_at: datetime = Field(
        ...,
        description='Data de criação do registro'
    )
