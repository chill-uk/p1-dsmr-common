from decimal import Decimal

from p1_dsmr_common.fluvius import DemandPeak, parse_demand_history


def test_parses_fluvius_demand_history() -> None:
    groups = (
        "2",
        "1-0:1.6.0",
        "1-0:1.6.0",
        "2026-09",
        "260930220000S",
        "3.125*kW",
        "2026-08",
        "260831220000S",
        "2.500*kW",
    )

    assert parse_demand_history(groups) == (
        DemandPeak("2026-09", "260930220000S", Decimal("3.125")),
        DemandPeak("2026-08", "260831220000S", Decimal("2.500")),
    )


def test_rejects_malformed_history() -> None:
    assert parse_demand_history(("1", "wrong", "shape", "x", "y", "1*kW")) == ()
