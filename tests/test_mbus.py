from p1_dsmr_common.mbus import (
    classify_mbus_measurement,
    get_mbus_field,
    mbus_device_type_name,
    normalize_device_type,
)


def test_classifies_common_mbus_measurements() -> None:
    assert classify_mbus_measurement(3, "m3") == "gas"
    assert classify_mbus_measurement("7", "m3") == "water"
    assert classify_mbus_measurement(3, "kWh") == "energy"
    assert classify_mbus_measurement(4, "GJ") == "energy"
    assert classify_mbus_measurement(4, "m3") is None


def test_normalizes_device_types() -> None:
    assert normalize_device_type("003") == 3
    assert normalize_device_type(7) == 7
    assert normalize_device_type(True) is None
    assert normalize_device_type("bad") is None


def test_device_type_name() -> None:
    assert mbus_device_type_name(3) == "Gas meter"
    assert mbus_device_type_name("7") == "Water meter"
    assert mbus_device_type_name(99) == "Type 99"



def test_version_specific_upstream_mbus_fields() -> None:
    """DSMR 4 gas and DSMR 5 generic M-Bus fields resolve identically."""
    from decimal import Decimal
    from types import SimpleNamespace

    def field(value: object, unit: str | None = None) -> SimpleNamespace:
        return SimpleNamespace(value=value, unit=unit)

    v4 = SimpleNamespace(
        DEVICE_TYPE=field(3),
        EQUIPMENT_IDENTIFIER_GAS=field("synthetic-gas-id"),
        HOURLY_GAS_METER_READING=field(Decimal("12334.675"), "m3"),
    )
    v5 = SimpleNamespace(
        MBUS_DEVICE_TYPE=field(3),
        MBUS_EQUIPMENT_IDENTIFIER=field("synthetic-gas-id"),
        MBUS_METER_READING=field(Decimal("11152.719"), "m3"),
    )
    for device, expected in ((v4, Decimal("12334.675")), (v5, Decimal("11152.719"))):
        assert get_mbus_field(device, "MBUS_DEVICE_TYPE").value == 3
        assert get_mbus_field(device, "MBUS_EQUIPMENT_IDENTIFIER").value == "synthetic-gas-id"
        reading = get_mbus_field(device, "MBUS_METER_READING")
        assert reading.value == expected
        assert reading.unit == "m3"
    assert get_mbus_field(v4, "UNKNOWN") is None



def test_gas_specific_legacy_names_never_apply_to_water_or_heat() -> None:
    """Gas-only legacy attributes must not become generic measurements."""
    from decimal import Decimal
    from types import SimpleNamespace

    for device_type in (4, 7, 10, 99):
        device = SimpleNamespace(
            DEVICE_TYPE=SimpleNamespace(value=device_type),
            EQUIPMENT_IDENTIFIER_GAS=SimpleNamespace(value="not-a-water-or-heat-id"),
            HOURLY_GAS_METER_READING=SimpleNamespace(
                value=Decimal("123.45"), unit="m3"
            ),
        )
        assert get_mbus_field(device, "MBUS_METER_READING") is None
        assert get_mbus_field(device, "MBUS_EQUIPMENT_IDENTIFIER") is None

    # Preserve DSMR 5's generic readings for water and heat.
    for device_type, unit in ((7, "m3"), (4, "GJ")):
        reading = SimpleNamespace(value=Decimal("50.25"), unit=unit)
        device = SimpleNamespace(
            MBUS_DEVICE_TYPE=SimpleNamespace(value=device_type),
            MBUS_METER_READING=reading,
        )
        assert get_mbus_field(device, "MBUS_METER_READING") is reading


def test_gas_specific_fallback_requires_valid_device_type() -> None:
    from types import SimpleNamespace

    device = SimpleNamespace(
        HOURLY_GAS_METER_READING=SimpleNamespace(value="123.45")
    )
    assert get_mbus_field(device, "MBUS_METER_READING") is None
