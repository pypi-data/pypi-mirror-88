from enum import Enum
from pydantic import BaseModel
from typing import TYPE_CHECKING, Generic, List, Optional, TypeVar, Union
from holon.ietf.rfc2119 import Keyword

if TYPE_CHECKING:
    from dataclasses import dataclass as autocomplete
else:

    def autocomplete(model):
        return model


T = TypeVar("T")
S = TypeVar("S")


@autocomplete
class Definition(BaseModel):
    name: str
    reference: Optional[str] = None


@autocomplete
class DefinitionRule(BaseModel):
    requirement: Keyword


@autocomplete
class Convention(Definition):
    pass


@autocomplete
class ConventionRule(DefinitionRule, Generic[T]):
    requirement: Keyword
    convention: Convention
    subject: Union[T, List[T]]


@autocomplete
class Ruleset(BaseModel):
    pass
