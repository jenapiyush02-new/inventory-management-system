from pydantic import BaseModel
from uuid import UUID

class WarehouseCreate(BaseModel):
    name: str
    location: str


class WarehouseResponse(BaseModel):
    id: UUID
    name: str
    location: str
    is_active: bool

    class Config:
        from_attributes = True