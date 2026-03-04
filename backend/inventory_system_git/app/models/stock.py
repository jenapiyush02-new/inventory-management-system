import uuid
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.db.session import Base
from sqlalchemy.orm import relationship

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    warehouse_id = Column(UUID(as_uuid=True), ForeignKey("warehouses.id"), nullable=False)
    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"), nullable=False)

    quantity = Column(Integer, default=0, nullable=False)

    item = relationship("Item")
    warehouse = relationship("Warehouse")
    __table_args__ = (
        UniqueConstraint("warehouse_id", "item_id", name="unique_stock_per_warehouse"),
    )