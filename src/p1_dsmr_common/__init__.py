"""Shared compatibility helpers layered on top of dsmr-parser."""

from .capabilities import new_capabilities
from .extensions import extended_spec
from .mappings import GLOBAL_MAPPING, resolve_mapping

__all__ = [
    "GLOBAL_MAPPING",
    "extended_spec",
    "new_capabilities",
    "resolve_mapping",
]
