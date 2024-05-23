"""Base models for API responses."""

import pydantic
from pydantic import alias_generators

__all__ = ["APIModel"]


class APIModel(pydantic.BaseModel):
    """Base model for API responses."""

    model_config = pydantic.ConfigDict(
        alias_generator=alias_generators.to_camel, populate_by_name=True, from_attributes=True
    )
