from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.sensor import router as sensor_router
from app.routers.mode import router as system_mode_router
from app.routers.thresholds import router as thresholds_router
from app.routers.feed_schedule import router as feed_schedule_router
from app.routers.device import router as device_state_router
from app.routers.history import router as history_router
from app.routers.event import router as event_router
from app.routers.notification import router as notification_router
from app.routers.camera import router as camera_router
from app.routers.system import router as system_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router, prefix="/api/v1")
app.include_router(sensor_router, prefix="/api/v1")
app.include_router(system_mode_router, prefix="/api/v1")
app.include_router(thresholds_router, prefix="/api/v1")
app.include_router(feed_schedule_router, prefix="/api/v1")
app.include_router(device_state_router, prefix="/api/v1")
app.include_router(history_router, prefix="/api/v1")
app.include_router(event_router, prefix="/api/v1")
app.include_router(notification_router, prefix="/api/v1")
app.include_router(camera_router, prefix="/api/v1")
app.include_router(system_router, prefix="/api/v1")