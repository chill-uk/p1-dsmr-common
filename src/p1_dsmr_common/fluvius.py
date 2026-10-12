"""Fluvius compatibility helpers layered on top of dsmr-parser."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from collections.abc import Sequence


@dataclass(frozen=True, slots=True)
class DemandPeak:
    """One raw Fluvius monthly demand-history record."""

    period: str
    timestamp: str
    peak_kw: Decimal


def parse_demand_history(groups: Sequence[str] | None) -> tuple[DemandPeak, ...]:
    """Parse Fluvius eMUCS-P1 13-month demand history groups.

    The caller supplies the raw value groups for OBIS 0-0:98.1.0. Raw local
    timestamps are intentionally preserved for compatibility and diagnostics.
    """
    if groups is None or len(groups) < 3:
        return ()

    count, first, second, *records = groups
    if not count.isascii() or not count.isdecimal():
        return ()
    if (first, second) != ("1-0:1.6.0", "1-0:1.6.0"):
        return ()
    if len(records) != int(count) * 3:
        return ()

    result: list[DemandPeak] = []
    for index in range(0, len(records), 3):
        period, timestamp, raw = records[index : index + 3]
        number, separator, unit = raw.rpartition("*")
        if not separator or unit != "kW":
            continue
        try:
            peak = Decimal(number)
        except (InvalidOperation, ValueError):
            continue
        if not peak.is_finite() or peak < 0:
            continue
        result.append(DemandPeak(period, timestamp, peak))

    return tuple(result)
