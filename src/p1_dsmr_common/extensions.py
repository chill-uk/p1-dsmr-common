"""Temporary dsmr-parser specification extensions."""

from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
from typing import Any

from dsmr_parser import obis_references as obis
from dsmr_parser.parsers import CosemParser, ValueParser


def extended_spec(base_spec: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of a dsmr-parser specification with shared extensions.

    Extensions should be removed from this package once the minimum supported
    dsmr-parser version provides them natively.
    """
    spec = deepcopy(base_spec)
    extensions = (
        ("ELECTRICITY_IMPORTED_TOTAL", getattr(obis, "ELECTRICITY_IMPORTED_TOTAL", None)),
        ("ELECTRICITY_EXPORTED_TOTAL", getattr(obis, "ELECTRICITY_EXPORTED_TOTAL", None)),
    )
    existing = {item["value_name"] for item in spec["objects"]}

    for value_name, reference in extensions:
        if reference is None or value_name in existing:
            continue
        spec["objects"].append(
            {
                "obis_reference": reference,
                "value_parser": CosemParser(ValueParser(Decimal)),
                "value_name": value_name,
            }
        )

    return spec
