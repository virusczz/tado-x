"""Helper methods for Tado."""

from .const import (
    CONST_OVERLAY_TADO_DEFAULT,
    CONST_OVERLAY_TADO_MODE,
    CONST_OVERLAY_TIMER,
)
from .coordinator import TadoDataUpdateCoordinator


def decide_overlay_mode(
    coordinator: TadoDataUpdateCoordinator,
    duration: int | None,
    zone_id: int,
    overlay_mode: str | None = None,
) -> str:
    """Return correct overlay mode based on the action and defaults."""

    # If user gave duration then overlay mode needs to be timer
    if duration:
        return CONST_OVERLAY_TIMER
    # If no duration or timer set to fallback setting
    if overlay_mode is None:
        overlay_mode = coordinator.fallback or CONST_OVERLAY_TADO_MODE
    # If default is Tado default then look it up
    if overlay_mode == CONST_OVERLAY_TADO_DEFAULT:
        overlay_mode = (
            coordinator.data["zone"][zone_id].default_overlay_termination_type
            or CONST_OVERLAY_TADO_MODE
        )

    return overlay_mode


def decide_duration(
    coordinator: TadoDataUpdateCoordinator,
    duration: int | None,
    zone_id: int,
    overlay_mode: str | None = None,
) -> None | int:
    """Return correct duration based on the selected overlay mode/duration and tado config."""

    # If we ended up with a timer but no duration, set a default duration
    # If we ended up with a timer but no duration, set a default duration
    if overlay_mode == CONST_OVERLAY_TIMER and duration is None:
        duration = (
            int(coordinator.data["zone"][zone_id].default_overlay_termination_duration)
            if coordinator.data["zone"][zone_id].default_overlay_termination_duration
            is not None
            else 3600
        )

    return duration


def generate_supported_fanmodes(
    tado_to_ha_mapping: dict[str, str], options: list[str]
) -> list[str] | None:
    """Return correct list of fan modes or None."""

    supported_fanmodes = [
        val for option in options if (val := tado_to_ha_mapping.get(option)) is not None
    ]
    if not supported_fanmodes:
        return None
    return supported_fanmodes
