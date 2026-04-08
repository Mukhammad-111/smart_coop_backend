from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.sensor import router as sensor_router


app = FastAPI()


app.include_router(auth_router, prefix="/api/v1")
app.include_router(sensor_router, prefix="/api/v1")