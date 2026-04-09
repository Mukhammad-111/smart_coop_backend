from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.sensor import router as sensor_router
from app.routers.mode import router as system_mode_router
from app.routers.thresholds import router as thresholds_router
from app.routers.device import router as device_state_router
from app.routers.history import router as history_router
from app.routers.event import router as event_router


app = FastAPI()


app.include_router(auth_router, prefix="/api/v1")
app.include_router(sensor_router, prefix="/api/v1")
app.include_router(system_mode_router, prefix="/api/v1")
app.include_router(thresholds_router, prefix="/api/v1")
app.include_router(device_state_router, prefix="/api/v1")
app.include_router(history_router, prefix="/api/v1")
app.include_router(event_router, prefix="/api/v1")