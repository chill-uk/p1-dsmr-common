from p1_dsmr_common.capabilities import new_capabilities


def test_late_capabilities_are_discovered_once() -> None:
    known: set[str] = set()
    candidates = ("energy_import_total", "energy_export_total")

    assert new_capabilities({}, known, candidates) == ()

    data = {
        "power_import": 123.0,
        "energy_import_total": 10000.123,
        "energy_export_total": 500.456,
    }
    discovered = new_capabilities(data, known, candidates)

    assert discovered == ("energy_import_total", "energy_export_total")

    known.update(discovered)
    assert new_capabilities(data, known, candidates) == ()


def test_none_is_not_an_available_capability() -> None:
    assert new_capabilities(
        {"energy_import_total": None},
        set(),
        ("energy_import_total",),
    ) == ()
