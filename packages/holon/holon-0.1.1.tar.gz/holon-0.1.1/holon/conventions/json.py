from enum import Enum
from holon.base import autocomplete, Convention, ConventionRule


class JSONElement(Enum):
    ITEM = "ITEM"
    PROPERTY = "Property"
    VALUE = "Value"
    OBJECT = "Object"
    ARRAY = "Array"
    STRING = "String"
    NUMBER = "Number"
    NULL = "Null"


@autocomplete
class JSONConventionRule(ConventionRule[JSONElement]):
    pass


allow_null = Convention(name="Allow NULL")
