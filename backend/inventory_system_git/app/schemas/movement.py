from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class MovementResponse(BaseModel):
    id: UUID
    warehouse_id: UUID
    item_id: UUID
    quantity_change: int
    movement_type: str
    performed_by: UUID
    created_at: datetime

    class Config:
        from_attributes = True