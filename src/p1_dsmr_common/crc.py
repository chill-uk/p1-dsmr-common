"""DSMR CRC helpers for integrations that preserve exact telegram bytes."""

from __future__ import annotations

import re
from dataclasses import dataclass

_CRC = re.compile(r"!([0-9A-Fa-f]{4})(?:\r?\n)?$")


@dataclass(frozen=True, slots=True)
class CrcResult:
    """Result of validating a telegram's reported CRC."""

    reported: str | None
    calculated: str | None
    valid: bool
    error: str | None = None


def calculate_crc(data: bytes) -> int:
    """Calculate the CRC-16/ARC used by DSMR telegrams."""
    crc = 0x0000
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
    return crc


def validate_crc(telegram: str) -> CrcResult:
    """Validate a CRC without normalizing or otherwise changing the telegram."""
    match = _CRC.search(telegram)
    if match is None:
        return CrcResult(None, None, False, "missing or malformed CRC")
    try:
        payload = telegram[: match.start() + 1].encode("ascii")
    except UnicodeEncodeError:
        return CrcResult(match.group(1).upper(), None, False, "non-ASCII telegram")

    reported = match.group(1).upper()
    calculated = f"{calculate_crc(payload):04X}"
    return CrcResult(
        reported=reported,
        calculated=calculated,
        valid=reported == calculated,
        error=None if reported == calculated else "CRC mismatch",
    )
