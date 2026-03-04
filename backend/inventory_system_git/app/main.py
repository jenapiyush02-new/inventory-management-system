from app.db.session import engine
from app.models.user import User
from app.db.session import Base

# Base.metadata.create_all(bind=engine)

from fastapi import FastAPI
from app.api.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router)

from app.api.test import router as test_router
app.include_router(test_router)

from app.api.inventory import router as inventory_router

app.include_router(inventory_router)

'''
web socket
'''
from app.websocket.routes import router as ws_router
app.include_router(ws_router)

'''
Global Exception Handler
'''
from fastapi.responses import JSONResponse
from fastapi import Request


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": str(exc)
        }
    )

'''
Health end point
'''
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }