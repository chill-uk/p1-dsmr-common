"""Common DSMR M-Bus classification helpers."""

from __future__ import annotations

from typing import Literal

MbusMeasurementKind = Literal["energy", "gas", "water"]

ENERGY_UNITS = frozenset({"j", "kj", "mj", "gj", "wh", "kwh", "mwh"})

METER_TYPE_NAMES: dict[int, str] = {
    0: "Other",
    1: "Oil meter",
    2: "Electricity meter",
    3: "Gas meter",
    4: "Heat meter",
    5: "Steam meter",
    6: "Hot water meter",
    7: "Water meter",
    8: "Heat cost allocator",
    9: "Compressed air",
    10: "Cooling load meter (outlet)",
    11: "Cooling load meter (inlet)",
    12: "Heat (inlet)",
    13: "Heat/cooling",
    14: "Bus/system",
    15: "Unknown",
}



# Upstream dsmr-parser exposes DSMR 4 gas fields under the legacy names,
# while DSMR 5 uses generic M-Bus names. Preserve those upstream identifiers.
MBUS_FIELD_ALIASES: dict[str, tuple[str, ...]] = {
    "MBUS_DEVICE_TYPE": ("MBUS_DEVICE_TYPE", "DEVICE_TYPE"),
    "MBUS_EQUIPMENT_IDENTIFIER": (
        "MBUS_EQUIPMENT_IDENTIFIER", "EQUIPMENT_IDENTIFIER_GAS"
    ),
    "MBUS_METER_READING": (
        "MBUS_METER_READING", "HOURLY_GAS_METER_READING"
    ),
}


def get_mbus_field(device: object, name: str) -> object | None:
    """Retrieve an upstream field across DSMR versions without renaming it."""
    for field_name in MBUS_FIELD_ALIASES.get(name, (name,)):
        field = getattr(device, field_name, None)
        if field is not None:
            return field
    return None

def normalize_device_type(device_type: object) -> int | None:
    """Convert an M-Bus device type to an integer when possible."""
    if isinstance(device_type, bool):
        return None
    if isinstance(device_type, int):
        return device_type
    if isinstance(device_type, str):
        try:
            return int(device_type, 10)
        except ValueError:
            return None
    return None


def classify_mbus_measurement(
    device_type: object,
    unit: object,
) -> MbusMeasurementKind | None:
    """Classify a reading using its unit and DSMR M-Bus device type."""
    normalized_type = normalize_device_type(device_type)
    normalized_unit = unit.casefold() if isinstance(unit, str) else None

    if normalized_unit in ENERGY_UNITS:
        return "energy"
    if normalized_unit != "m3":
        return None
    if normalized_type == 3:
        return "gas"
    if normalized_type in {6, 7}:
        return "water"
    return None


def mbus_device_type_name(device_type: object) -> str | None:
    """Return the standard M-Bus device type label."""
    normalized = normalize_device_type(device_type)
    if normalized is None:
        return None
    return METER_TYPE_NAMES.get(normalized, f"Type {normalized}")
