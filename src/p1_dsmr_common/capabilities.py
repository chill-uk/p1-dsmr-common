"""Capability discovery helpers."""

from __future__ import annotations

from collections.abc import Iterable, Mapping


def new_capabilities(
    data: Mapping[str, object],
    known: set[str],
    candidates: Iterable[str] | None = None,
) -> tuple[str, ...]:
    """Return newly available capabilities in stable order.

    A capability is considered available only when the key exists and its value
    is not None. Entity creation remains the responsibility of the consuming
    integration.
    """
    ordered = tuple(candidates) if candidates is not None else tuple(data)
    return tuple(
        key
        for key in ordered
        if key in data and data[key] is not None and key not in known
    )
