from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.sensor import router as sensor_router
from app.routers.mode import router as system_mode_router
from app.routers.device import router as device_state_router


app = FastAPI()


app.include_router(auth_router, prefix="/api/v1")
app.include_router(sensor_router, prefix="/api/v1")
app.include_router(system_mode_router, prefix="/api/v1")
app.include_router(device_state_router, prefix="/api/v1")