from pydantic import BaseModel, Field


class ThresholdsResponse(BaseModel):
    t_comfort_min: float
    t_comfort_max: float
    t_low_on: float
    t_low_off: float
    t_high_on: float
    t_high_off: float
    t_critical_low: float
    t_critical_high: float
    h_normal_max: float
    h_normal_min: float
    h_critical: float
    lux_day_on: int
    lux_day_off: int
    lux_light_on: int
    lux_light_off: int