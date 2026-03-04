from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.item import Item
from app.models.category import Category


'''
Implement Stock Update in Service Layer
'''
from app.models.stock import Stock
from app.models.inventory_movement import InventoryMovement, MovementType
from app.models.warehouse import Warehouse
from app.models.item import Item
from app.models.user_warehouse import UserWarehouse
from fastapi import HTTPException

from app.models.category import Category
from sqlalchemy.orm import joinedload


from app.websocket.manager import manager
import asyncio

from app.models.user import User
from app.core.logger import logger


class InventoryService:
    

    @staticmethod
    def generate_sku(db: Session, category: Category) -> str:
        """
        Generate SKU in format:
        CATEGORYCODE-00001
        """

        count = db.query(func.count(Item.id))\
                  .filter(Item.category_id == category.id)\
                  .scalar()

        next_number = count + 1

        return f"{category.code}-{next_number:05d}"

    @staticmethod
    def create_item(db: Session, name: str, category_id, description: str = None):

        # Validate category
        category = db.query(Category).filter(
        Category.id == category_id,
        Category.is_active == True
    ).first()

        if not category:
            raise HTTPException(status_code=400, detail="Invalid or inactive category")

        # Generate SKU
        sku = InventoryService.generate_sku(db, category)

        item = Item(
            name=name,
            sku=sku,
            category_id=category_id,
            description=description
        )

        db.add(item)
        try:
            db.commit()
            db.refresh(item)
        except Exception:
            db.rollback()
            raise HTTPException(status_code=500, detail="Failed to create item")

        logger.info(f"Item created: {item.id} - {item.name}")
        
        return item
    
    @staticmethod
    def update_stock(db: Session, user, warehouse_id, item_id, quantity, movement_type):

        warehouse = db.query(Warehouse).filter(
            Warehouse.id == warehouse_id,
            Warehouse.is_active == True
        ).first()

        if not warehouse:
            raise HTTPException(status_code=404, detail="Warehouse not found")

        item = db.query(Item).filter(
            Item.id == item_id,
            Item.is_active == True
        ).first()

        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        # Authorization check
        if user.role == "manager":
            mapping = db.query(UserWarehouse).filter(
                UserWarehouse.user_id == user.id,
                UserWarehouse.warehouse_id == warehouse_id
            ).first()

            if not mapping:
                raise HTTPException(status_code=403, detail="Not assigned to this warehouse")

        if user.role == "viewer":
            raise HTTPException(status_code=403, detail="Viewer cannot modify stock")

        # Get or create stock row
        # Lock stock row
        stock = db.query(Stock).filter(
            Stock.warehouse_id == warehouse_id,
            Stock.item_id == item_id).with_for_update().first()


        if not stock:
            stock = Stock(
                warehouse_id=warehouse_id,
                item_id=item_id,
                quantity=0
            )
            db.add(stock)
            db.flush()

        if movement_type == MovementType.IN:
            stock.quantity += quantity

        elif movement_type == MovementType.OUT:
            if stock.quantity < quantity:
                raise HTTPException(status_code=400, detail="Insufficient stock")
            stock.quantity -= quantity

        elif movement_type == MovementType.ADJUST:
            stock.quantity = quantity

        movement = InventoryMovement(
            warehouse_id=warehouse_id,
            item_id=item_id,
            quantity_change=quantity if movement_type != MovementType.OUT else -quantity,
            movement_type=movement_type,
            performed_by=user.id
        )

        db.add(movement)
        db.commit()
        db.refresh(stock)

        #broadcast
        try:
            import asyncio
            from app.websocket.manager import manager

            loop = asyncio.get_event_loop()
            loop.create_task(
            manager.broadcast({
                "warehouse_id": str(warehouse_id),
                "item_id": str(item_id),
                "new_quantity": stock.quantity
            }))
        except RuntimeError:
            pass # No active event loop
            
        
        logger.info(
    f"Stock updated | Warehouse: {warehouse_id} | "
    f"Item: {item_id} | New Qty: {stock.quantity} | "
    f"By User: {user.id}"
)
        
        return stock
    
    @staticmethod
    def get_warehouse_inventory(db: Session, user, warehouse_id):

        warehouse = db.query(Warehouse).filter(
            Warehouse.id == warehouse_id,
            Warehouse.is_active == True
        ).first()

        if not warehouse:
            raise HTTPException(status_code=404, detail="Warehouse not found")

        # Authorization
        if user.role == "manager":
            mapping = db.query(UserWarehouse).filter(
                UserWarehouse.user_id == user.id,
                UserWarehouse.warehouse_id == warehouse_id
            ).first()

            if not mapping:
                raise HTTPException(status_code=403, detail="Not assigned to this warehouse")

        if user.role == "viewer":
            pass  # viewers can read

        stocks = db.query(Stock)\
            .options(joinedload(Stock.item))\
            .filter(Stock.warehouse_id == warehouse_id)\
            .all()

        result = []

        for stock in stocks:
            result.append({
                "item_id": stock.item.id,
                "item_name": stock.item.name,
                "sku": stock.item.sku,
                "category": stock.item.category.name,
                "quantity": stock.quantity
            })

        return result
    

    @staticmethod
    def get_warehouse_summary(db: Session, user, warehouse_id):

        # reuse authorization logic
        inventory = InventoryService.get_warehouse_inventory(db, user, warehouse_id)

        total_items = len(inventory)
        total_quantity = sum(item["quantity"] for item in inventory)

        low_stock = [
            item for item in inventory if item["quantity"] < 10
        ]

        return {
            "total_items": total_items,
            "total_quantity": total_quantity,
            "low_stock_count": len(low_stock)
        }
        

# Create warehouse

    @staticmethod
    def create_warehouse(db: Session, name: str, location: str):

        existing = db.query(Warehouse).filter(
        Warehouse.name == name).first()

        if existing:
            raise HTTPException(status_code=400, detail="Warehouse already exists")

        warehouse = Warehouse(
        name=name,
        location=location)

        db.add(warehouse)
        db.commit()
        db.refresh(warehouse)

        return warehouse
    
# Assign Manager to Warehouse
    @staticmethod
    def assign_manager(db: Session, user_id, warehouse_id):

        user = db.query(User).filter(
        User.id == user_id,
        User.role == "manager"
    ).first()

        if not user:
            raise HTTPException(status_code=404, detail="Manager not found")

        warehouse = db.query(Warehouse).filter(
        Warehouse.id == warehouse_id
    ).first()

        if not warehouse:
            raise HTTPException(status_code=404, detail="Warehouse not found")

        existing = db.query(UserWarehouse).filter(
        UserWarehouse.user_id == user_id,
        UserWarehouse.warehouse_id == warehouse_id
    ).first()

        if existing:
            raise HTTPException(status_code=400, detail="Already assigned")

        mapping = UserWarehouse(
        user_id=user_id,
        warehouse_id=warehouse_id
    )

        db.add(mapping)
        db.commit()
        
        logger.info(
    f"Manager {user_id} assigned to warehouse {warehouse_id}"
)

        return {"message": "Manager assigned successfully"}

# List Warehouses (Role-aware)
    @staticmethod
    def list_warehouses(db: Session, user):

        if user.role == "admin":
            return db.query(Warehouse).filter(
            Warehouse.is_active == True).all()

        if user.role == "manager":
            mappings = db.query(UserWarehouse).filter(
            UserWarehouse.user_id == user.id).all()

            warehouse_ids = [m.warehouse_id for m in mappings]

            return db.query(Warehouse).filter(Warehouse.id.in_(warehouse_ids),
            Warehouse.is_active == True).all()

        if user.role == "viewer":
            return db.query(Warehouse).filter(
            Warehouse.is_active == True).all()
            
#  Dashboard Summary

    @staticmethod
    def warehouse_summary(db: Session, warehouse_id):

        results = (
        db.query(
            Item.name,
            Stock.quantity
        )
        .join(Stock, Stock.item_id == Item.id)
        .filter(
            Stock.warehouse_id == warehouse_id,
            Item.is_active == True
        )
        .all()
    )

        return results
    
#Low Stock Alert API
 
    @staticmethod
    def low_stock_items(db: Session, threshold: int = 10):

        return (
        db.query(Stock)
        .filter(Stock.quantity <= threshold)
        .all())
        
# Deactivate APIs
    @staticmethod
    def deactivate_item(db: Session, item_id):

        item = db.query(Item).filter(
        Item.id == item_id,
        Item.is_active == True
        ).first()

        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        item.is_active = False
        db.commit()

        logger.info(f"Item deactivated: {item_id}")
        
        return {"message": "Item deactivated"}
    
    @staticmethod
    def movement_history(db: Session, item_id=None, warehouse_id=None):

        query = db.query(InventoryMovement)

        if item_id:
            query = query.filter(InventoryMovement.item_id == item_id)

        if warehouse_id:
            query = query.filter(InventoryMovement.warehouse_id == warehouse_id)

        return query.order_by(
            InventoryMovement.created_at.desc()).all()
        
    @staticmethod
    def list_items(db: Session, skip: int = 0, limit: int = 10):
        return (
        db.query(Item)
        .filter(Item.is_active == True)
        .offset(skip)
        .limit(limit)
        .all()
    )
        
    