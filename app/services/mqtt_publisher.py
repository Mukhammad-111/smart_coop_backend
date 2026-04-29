import json

client = None

def set_mqtt_client(mqtt_client):
    global client
    client = mqtt_client


async def publish_command(command: dict):
    if client is None:
        print("MQTT client not set")
        return

    try:
        client.publish("coop/commands", json.dumps(command), qos=1)
    except Exception as e:
        print("MQTT publish error:", e)