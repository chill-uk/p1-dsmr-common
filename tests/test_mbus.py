from p1_dsmr_common.mbus import (
    classify_mbus_measurement,
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
