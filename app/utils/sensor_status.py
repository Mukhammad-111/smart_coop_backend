from app.schemas.sensor import TemperatureStatus, HumidityStatus, LightStatus


def get_temperature_status(temp: float | None, threshold) -> TemperatureStatus:
    if temp is None:
        return TemperatureStatus.sensor_error
    if temp <= threshold.t_critical_low:
        return TemperatureStatus.critical_low
    if temp >= threshold.t_critical_high:
        return TemperatureStatus.critical_high

    if temp <= threshold.t_low_on:
        return TemperatureStatus.low

    if temp >= threshold.t_high_on:
        return TemperatureStatus.high

    if threshold.t_comfort_min <= temp <= threshold.t_comfort_max:
        return TemperatureStatus.normal

    if temp <= threshold.t_comfort_min:
        return TemperatureStatus.low

    return TemperatureStatus.high


def get_humidity_status(hum: float | None, threshold) -> HumidityStatus:
    if hum is None:
        return HumidityStatus.sensor_error
    if hum >= threshold.h_critical:
        return HumidityStatus.critical
    if hum > threshold.h_normal_max:
        return HumidityStatus.high
    return HumidityStatus.normal


def get_light_status(lux: int | None, threshold) -> LightStatus:
    if lux is None:
        return LightStatus.sensor_error
    if lux >= threshold.lux_day_on:
        return LightStatus.bright
    if lux < threshold.lux_day_off:
        return LightStatus.dark
    return LightStatus.normal