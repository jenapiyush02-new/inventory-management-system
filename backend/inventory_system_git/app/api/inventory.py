from fastapi import APIRouter, Depends, HTTPException, logger
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models import warehouse
from app.schemas.item import ItemCreate, ItemResponse
from app.services.inventory_service import InventoryService
from app.core.security import require_role
from app.schemas.base import APIResponse


router = APIRouter(prefix="/items", tags=["Items"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=APIResponse[ItemResponse])
def create_item(
    item_data: ItemCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),
):
    item = InventoryService.create_item(
        db=db,
        name=item_data.name,
        category_id=item_data.category_id,
        description=item_data.description,
    )

    return APIResponse(
        success=True,
        message="Item created successfully",
        data=item
    )
    
'''
Inventory Movement
'''
    
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.item import ItemCreate, ItemResponse
from app.schemas.stock import StockResponse, StockUpdateRequest
from app.services.inventory_service import InventoryService
from app.core.security import require_role, get_current_user

from app.schemas.stock import StockUpdateRequest
from app.models.stock import Stock


@router.post("/stock", response_model=APIResponse[dict])
def update_stock(
    request: StockUpdateRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    stock = InventoryService.update_stock(
        db=db,
        user=user,
        warehouse_id=request.warehouse_id,
        item_id=request.item_id,
        quantity=request.quantity,
        movement_type=request.movement_type
    )

    return APIResponse(
    success=True,
    message="Stock updated successfully",
    data={
        "warehouse_id": stock.warehouse_id,
        "item_id": stock.item_id,
        "new_quantity": stock.quantity
    }
)

from app.schemas.dashboard import WarehouseInventoryItem


@router.get("/warehouse/{warehouse_id}")
def get_inventory(
    warehouse_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    data = InventoryService.get_warehouse_inventory(
        db=db,
        user=user,
        warehouse_id=warehouse_id
    )

    return data

# @router.get("/warehouse/{warehouse_id}/summary")
# def get_summary(
#     warehouse_id: str,
#     db: Session = Depends(get_db),
#     user=Depends(get_current_user)
# ):
#     return InventoryService.get_warehouse_summary(
#         db=db,
#         user=user,
#         warehouse_id=warehouse_id
#     )
    
    
# Create Warehouse
from app.schemas.warehouse import WarehouseCreate, WarehouseResponse


@router.post("/warehouse", response_model=APIResponse[WarehouseResponse])
def create_warehouse(
    data: WarehouseCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    warehouse = InventoryService.create_warehouse(
        db=db,
        name=data.name,
        location=data.location
    )

    return APIResponse(
        success=True,
        message="Warehouse created successfully",
        data=warehouse
    )
    
# Assign Manager 

from uuid import UUID

@router.post(
    "/warehouse/{warehouse_id}/assign/{user_id}",
    response_model=APIResponse[dict]
)
def assign_manager(
    warehouse_id: UUID,
    user_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    InventoryService.assign_manager(db, user_id, warehouse_id)

    return APIResponse(
        success=True,
        message="Manager assigned successfully",
        data=None
    )
    
# List Warehouse
@router.get("/warehouse", response_model=list[WarehouseResponse])
def get_warehouses(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return InventoryService.list_warehouses(db=db, user=user)

# Dashboard Summary

@router.get("/warehouse/{warehouse_id}/summary")
def get_warehouse_summary(
    warehouse_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)):
    
    InventoryService.warehouse_summary(db, warehouse_id)
    
    return APIResponse(
    success=True,
    message="Item deactivated successfully",
    data=None
)

# Low Stock Api

@router.get("/low-stock")
def low_stock(
    threshold: int = 10,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)):
    
    return InventoryService.low_stock_items(db, threshold)

# DEACTIVATE API
@router.delete("/item/{item_id}", response_model=APIResponse[dict])
def deactivate_item(
    item_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    InventoryService.deactivate_item(db, item_id)

    return APIResponse(
        success=True,
        message="Item deactivated successfully",
        data=None
    )


from app.models.item import Item


    
# audit 
@router.get("/movements")
def get_movements(
    item_id: UUID = None,
    warehouse_id: UUID = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return InventoryService.movement_history(
        db,
        item_id=item_id,
        warehouse_id=warehouse_id
    )
    

# get all
@router.get("/items")
def list_items(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return InventoryService.list_items(db, skip, limit)



from app.schemas.movement import MovementResponse
@router.get("/movements", response_model=list[MovementResponse])
def get_movements(
    item_id: UUID = None,
    warehouse_id: UUID = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return InventoryService.movement_history(
        db,
        item_id=item_id,
        warehouse_id=warehouse_id
    )

'''
@router.get("/items")
def list_items(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return (
        db.query(Item)
        .filter(Item.is_active == True)
        .offset(skip)
        .limit(limit)
        .all()
    )
'''