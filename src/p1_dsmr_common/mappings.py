"""Neutral capability mappings for dsmr-parser values."""

from __future__ import annotations

from collections.abc import Mapping

GLOBAL_MAPPING: dict[str, str] = {
    "ELECTRICITY_IMPORTED_TOTAL": "energy_import_total",
    "ELECTRICITY_EXPORTED_TOTAL": "energy_export_total",
    "ELECTRICITY_USED_TARIFF_1": "energy_import_tariff_1",
    "ELECTRICITY_USED_TARIFF_2": "energy_import_tariff_2",
    "ELECTRICITY_DELIVERED_TARIFF_1": "energy_export_tariff_1",
    "ELECTRICITY_DELIVERED_TARIFF_2": "energy_export_tariff_2",
    "CURRENT_ELECTRICITY_USAGE": "power_import",
    "CURRENT_ELECTRICITY_DELIVERY": "power_export",
    "INSTANTANEOUS_ACTIVE_POWER_L1_POSITIVE": "power_import_l1",
    "INSTANTANEOUS_ACTIVE_POWER_L2_POSITIVE": "power_import_l2",
    "INSTANTANEOUS_ACTIVE_POWER_L3_POSITIVE": "power_import_l3",
    "INSTANTANEOUS_ACTIVE_POWER_L1_NEGATIVE": "power_export_l1",
    "INSTANTANEOUS_ACTIVE_POWER_L2_NEGATIVE": "power_export_l2",
    "INSTANTANEOUS_ACTIVE_POWER_L3_NEGATIVE": "power_export_l3",
    "INSTANTANEOUS_CURRENT_L1": "current_l1",
    "INSTANTANEOUS_CURRENT_L2": "current_l2",
    "INSTANTANEOUS_CURRENT_L3": "current_l3",
    "INSTANTANEOUS_VOLTAGE_L1": "voltage_l1",
    "INSTANTANEOUS_VOLTAGE_L2": "voltage_l2",
    "INSTANTANEOUS_VOLTAGE_L3": "voltage_l3",
    "VOLTAGE_SAG_L1_COUNT": "voltage_sags_l1",
    "VOLTAGE_SAG_L2_COUNT": "voltage_sags_l2",
    "VOLTAGE_SAG_L3_COUNT": "voltage_sags_l3",
    "VOLTAGE_SWELL_L1_COUNT": "voltage_swells_l1",
    "VOLTAGE_SWELL_L2_COUNT": "voltage_swells_l2",
    "VOLTAGE_SWELL_L3_COUNT": "voltage_swells_l3",
    "SHORT_POWER_FAILURE_COUNT": "power_failures",
    "LONG_POWER_FAILURE_COUNT": "long_power_failures",
    "ELECTRICITY_ACTIVE_TARIFF": "tariff_indicator",
}


def resolve_mapping(
    upstream_name: str,
    local_mapping: Mapping[str, str] | None = None,
) -> str | None:
    """Resolve a dsmr-parser field using local overrides before global defaults."""
    if local_mapping is not None and upstream_name in local_mapping:
        return local_mapping[upstream_name]
    return GLOBAL_MAPPING.get(upstream_name)
