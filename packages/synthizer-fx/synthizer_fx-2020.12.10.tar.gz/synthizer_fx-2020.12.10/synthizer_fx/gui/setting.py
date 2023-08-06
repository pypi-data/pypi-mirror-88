"""Provides the Setting class."""

from typing import Optional

from attr import attrs


@attrs(auto_attribs=True)
class Bounds:
    """Bounds for a setting."""

    min: float
    max: float


@attrs(auto_attribs=True)
class Setting:
    """A setting for an effect."""

    name: str
    description: str
    bounds: Optional[Bounds] = None
