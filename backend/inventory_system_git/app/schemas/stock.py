from pydantic import BaseModel
from uuid import UUID
from enum import Enum


class MovementType(str, Enum):
    IN = "IN"
    OUT = "OUT"
    ADJUST = "ADJUST"


class StockUpdateRequest(BaseModel):
    warehouse_id: UUID
    item_id: UUID
    quantity: int
    movement_type: MovementType
    
class StockResponse(BaseModel):
    warehouse_id: UUID
    item_id: UUID
    quantity: int