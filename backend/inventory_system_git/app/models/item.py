import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.session import Base
from sqlalchemy.orm import relationship

class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String(150), unique=True, nullable=False)
    sku = Column(String(50), unique=True, nullable=False)

    category_id = Column(
        UUID(as_uuid=True),
        ForeignKey("categories.id"),   # ← THIS IS CRITICAL
        nullable=False
    )

    description = Column(String(255))
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    category = relationship("Category")