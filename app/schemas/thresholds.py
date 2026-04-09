from pydantic import BaseModel, Field, model_validator


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

    @model_validator(mode="after")
    def validate_thresholds(self):
        if self.t_comfort_min >= self.t_comfort_max:
            raise ValueError("t_comfort_min must be < t_comfort_max")

        if not (self.t_low_on < self.t_low_off <= self.t_comfort_min):
            raise ValueError("Invalid low temperature thresholds")

        if not (self.t_comfort_max < self.t_high_off < self.t_high_on):
            raise ValueError("Invalid high temperature thresholds")

        if self.t_critical_low >= self.t_low_on:
            raise ValueError("t_critical_low must be < t_low_on")

        if self.t_high_on >= self.t_critical_high:
            raise ValueError("t_high_on must be < t_critical_high")

        if self.lux_day_off >= self.lux_day_on:
            raise ValueError("lux_day_off must be < lux_day_on")

        if self.lux_light_on >= self.lux_light_off:
            raise ValueError("lux_light_on must be < lux_light_off")

        return self


class ThresholdsUpdateRequest(BaseModel):
    t_comfort_min: float | None = None
    t_comfort_max: float | None = None
    t_low_on: float | None = None
    t_low_off: float | None = None
    t_high_on: float | None = None
    t_high_off: float | None = None
    t_critical_low: float | None = None
    t_critical_high: float | None = None
    h_normal_max: float | None = None
    h_normal_min: float | None = None
    h_critical: float | None = None
    lux_day_on: int | None = None
    lux_day_off: int | None = None
    lux_light_on: int | None = None
    lux_light_off: int | None = None