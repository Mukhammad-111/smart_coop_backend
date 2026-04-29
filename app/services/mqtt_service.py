from gmqtt import Client as MQTTClient
import json
import asyncio

from app.database.session import async_session_local
from app.repositories.user import UserRepository
from app.schemas.device import DeviceStateRequest
from app.schemas.sensor import SensorDataRequest
from app.services.device_state import device_state_create_service
from app.services.mqtt_publisher import set_mqtt_client
from app.services.sensor_service import sensor_data_service

MQTT_BROKER = "localhost"
MQTT_PORT = 1883


client = MQTTClient("backend")


async def handle_sensor_message(payload: bytes):
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        print("Invalid JSON")
        return

    api_key = data.get("api_key")
    if not api_key:
        print("No API Key")
        return

    async with async_session_local() as db:
        user = await UserRepository.get_by_api_key(api_key, db)
        if not user:
            print("Invalid API Key")
            return

        sensor = SensorDataRequest(
            temperature=data.get("temperature"),
            humidity=data.get("humidity"),
            light_level=data.get("light_level"),
        )

        await sensor_data_service(sensor, db, user.id)


async def handle_device_message(payload: bytes):
    data = json.loads(payload)

    async with async_session_local() as db:
        device = DeviceStateRequest(**data)
        await device_state_create_service(device, db)


def on_message(client, topic, payload, qos, properties):
    if topic == "coop/sensor":
        asyncio.create_task(handle_sensor_message(payload))

    elif topic == "coop/device/state":
        asyncio.create_task(handle_device_message(payload))


async def start_mqtt():
    client.on_message = on_message

    await client.connect(MQTT_BROKER, MQTT_PORT)

    set_mqtt_client(client)

    client.subscribe("coop/sensor", qos=1)
    client.subscribe("coop/device/state", qos=1)

    print("MQTT connected")