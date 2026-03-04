import uuid
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.session import Base


class Warehouse(Base):
    __tablename__="warehouses"

    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)

    name=Column(String(100),unique=True,nullable=False)

    location=Column(String(255),nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())