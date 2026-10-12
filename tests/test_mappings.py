from p1_dsmr_common.mappings import GLOBAL_MAPPING, resolve_mapping


def test_global_mapping_uses_neutral_names() -> None:
    assert GLOBAL_MAPPING["CURRENT_ELECTRICITY_USAGE"] == "power_import"
    assert GLOBAL_MAPPING["CURRENT_ELECTRICITY_DELIVERY"] == "power_export"


def test_local_mapping_overrides_global_mapping() -> None:
    local = {
        "CURRENT_ELECTRICITY_USAGE": "power_consumption",
        "CURRENT_ELECTRICITY_DELIVERY": "power_production",
    }

    assert resolve_mapping("CURRENT_ELECTRICITY_USAGE", local) == "power_consumption"
    assert resolve_mapping("CURRENT_ELECTRICITY_DELIVERY", local) == "power_production"
    assert resolve_mapping("ELECTRICITY_IMPORTED_TOTAL", local) == "energy_import_total"


def test_unknown_mapping_is_ignored() -> None:
    assert resolve_mapping("NOT_A_DSMR_FIELD") is None
