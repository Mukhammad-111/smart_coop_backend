from app.repositories.thresholds import ThresholdRepository


async def check_and_notify(
        temperature,
        humidity,
        thresholds,
        notif_settings):

    if temperature is not None:
        if temperature >= thresholds.t_high_on and notif_settings.notif_alarm_temp_high:
            print("🔥 HIGH TEMP ALERT")
    if temperature is not None:
        if temperature >= thresholds.h_critical and notif_settings.notif_alarm_humidity:
            print("💧 HIGH HUMIDITY ALERT")