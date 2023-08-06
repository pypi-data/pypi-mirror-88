from enum import Enum
from typing import Dict, ForwardRef, List, Literal, Optional, Union
from holon.base import autocomplete, Definition, DefinitionRule


@autocomplete
class Principle(Definition):
    pass


@autocomplete
class PrincipleRule(DefinitionRule):
    principle: Principle


robustness = Principle(
    name="Robustness Principle",
    reference="https://en.wikipedia.org/wiki/Robustness_principle",
)

# TODO: Further reading on downside
# https://tools.ietf.org/id/draft-thomson-postel-was-wrong-03.html

yagni = Principle(name="YAGNI", reference="https://martinfowler.com/bliki/Yagni.html")

# TODO: find good link for these
# TODO: move to practice
design_first = Principle(name="Design First")
code_first = Principle(name="Code First")
api_first = Principle(name="API First")
