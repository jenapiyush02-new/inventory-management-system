from pydantic import BaseModel
from uuid import UUID


class WarehouseInventoryItem(BaseModel):
    item_id: UUID
    item_name: str
    sku: str
    category: str
    quantity: int

    class Config:
        from_attributes = True