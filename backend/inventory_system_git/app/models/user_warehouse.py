import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.session import Base

class UserWarehouse(Base):
    __tablename__="user_warehouses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id=Column(UUID(as_uuid=True),ForeignKey("users.id"),nullable=False)
    warehouse_id=Column(UUID(as_uuid=True),ForeignKey("warehouses.id"),nullable=False)