from pydantic import BaseModel
from uuid import UUID


class ItemCreate(BaseModel):
    name: str
    category_id: UUID
    description: str | None = None


class ItemResponse(BaseModel):
    id: UUID
    name: str
    sku: str
    category_id: UUID
    description: str | None
    is_active: bool

    class Config:
        from_attributes = True