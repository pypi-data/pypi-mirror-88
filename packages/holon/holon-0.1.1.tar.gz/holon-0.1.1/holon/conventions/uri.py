from enum import Enum
from holon.base import autocomplete, Convention, ConventionRule


@autocomplete
class URIElement(Enum):
    RESOURCE_NAME = "Resource Name"
    TEMPLATES = "Templates"


@autocomplete
class URIConventionRule(ConventionRule[URIElement]):
    pass


nest_resources = Convention(name="Nest Resources")
include_version = Convention(name="Include Version")
uuid_as_id = Convention(name="UUID as ID")
