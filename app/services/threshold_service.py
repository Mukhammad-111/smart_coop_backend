from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.thresholds import ThresholdRepository
from app.schemas.thresholds import ThresholdsResponse


async def get_current_thresholds(db: AsyncSession) -> ThresholdsResponse:
    thresholds = await ThresholdRepository.get_active(db)
    if thresholds is None:
        return ThresholdsResponse(
            t_comfort_min=18.0,
            t_comfort_max=24.0,
            t_low_on=10.0,
            t_low_off=12.0,
            t_high_on=30.0,
            t_high_off=28.0,
            t_critical_low=3.0,
            t_critical_high=35.0,
            h_normal_max=70.0,
            h_normal_min=60.0,
            h_critical=85.0,
            lux_day_on=200,
            lux_day_off=150,
            lux_light_on=300,
            lux_light_off=350
        )
    return ThresholdsResponse.model_validate(thresholds)