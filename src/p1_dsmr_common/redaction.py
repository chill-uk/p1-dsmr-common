"""Helpers for safely redacting meter identifiers from diagnostic telegrams."""

from __future__ import annotations

import re

_EQUIPMENT_ID = re.compile(r"^(0-\d+:96\.1\.[01])\([^()]*\)\r?$", re.MULTILINE)


def redact_equipment_ids(telegram: str) -> str:
    """Redact electricity and M-Bus equipment IDs without changing other lines."""
    return _EQUIPMENT_ID.sub(r"\1(<redacted>)", telegram)
