from app.db.session import SessionLocal
from app.models.category import Category
from app.models.warehouse import Warehouse
from app.models.user import User, UserRole
from app.models.user_warehouse import UserWarehouse
from app.core.security import hash_password


def seed():
    db = SessionLocal()

    # Create Category
    if not db.query(Category).first():
        electronics = Category(
            name="Electronics",
            code="ELEC",
            description="Electronic Items"
        )
        db.add(electronics)

    # Create Warehouse
    if not db.query(Warehouse).first():
        warehouse = Warehouse(
            name="Main Warehouse",
            location="Mumbai"
        )
        db.add(warehouse)

    db.commit()

    # Create Admin
    if not db.query(User).filter(User.username == "admin").first():
        admin = User(
            username="admin",
            email="admin@test.com",
            password_hash=hash_password("admin123"),
            role=UserRole.admin
        )
        db.add(admin)

    # Create Manager
    if not db.query(User).filter(User.username == "manager").first():
        manager = User(
            username="manager",
            email="manager@test.com",
            password_hash=hash_password("manager123"),
            role=UserRole.manager
        )
        db.add(manager)

    db.commit()

    # Assign Manager to Warehouse
    manager = db.query(User).filter(User.username == "manager").first()
    warehouse = db.query(Warehouse).first()

    if manager and warehouse:
        if not db.query(UserWarehouse).filter(
            UserWarehouse.user_id == manager.id,
            UserWarehouse.warehouse_id == warehouse.id
        ).first():
            mapping = UserWarehouse(
                user_id=manager.id,
                warehouse_id=warehouse.id
            )
            db.add(mapping)

    db.commit()
    db.close()

    print("Seeding completed.")


if __name__ == "__main__":
    seed()