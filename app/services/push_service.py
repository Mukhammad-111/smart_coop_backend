from app.models import User


async def check_and_notify(
        temperature,
        humidity,
        thresholds,
        user
):
    alerts = []

    if temperature is None:
        alerts.append("sensor_error_temp")

    else:
        if temperature >= thresholds.t_critical_high:
            if user.notif_alarm_temp_high:
                alerts.append("critical_high_temp")

        elif temperature <= thresholds.t_critical_low:
            if user.notif_alarm_temp_low:
                alerts.append("critical_low_temp")

        elif temperature >= thresholds.t_high_on:
            if user.notif_alarm_temp_high:
                alerts.append("high_temp")

        elif temperature <= thresholds.t_low_on:
            if user.notif_alarm_temp_low:
                alerts.append("low_temp")

    if humidity is None:
        alerts.append("sensor_error_humidity")

    else:
        if humidity >= thresholds.h_critical:
            if user.notif_alarm_humidity:
                alerts.append("critical_humidity")

        elif humidity > thresholds.h_normal_max:
            if user.notif_alarm_humidity:
                alerts.append("high_humidity")

    for alert in alerts:
        await send_push(alert, user)


async def send_push(event: str, user: User):
    print(f"📲 PUSH → {event} for user {user.id}")