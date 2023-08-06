from enum import Enum
from http import HTTPStatus
from typing import List, Optional, Union
from holon.base import autocomplete, ConventionRule, Definition, DefinitionRule, Ruleset


class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"


class HTTPMessage(Enum):
    REQUEST = "request"
    RESPONSE = "response"


class HTTPHeader(Enum):
    NAME = "Name"
    VALUE = "Value"


@autocomplete
class Header(Definition):
    pass


@autocomplete
class HeaderRule(DefinitionRule):
    header: Header


@autocomplete
class MediaType(Definition):
    pass


@autocomplete
class MediaTypeRule(DefinitionRule):
    media_type: MediaType


@autocomplete
class HTTPConventionRule(
    ConventionRule[Union[HTTPHeader, HTTPMessage, HTTPMethod, HTTPStatus]]
):
    pass


@autocomplete
class HTTPRuleSet(Ruleset):
    headers: Optional[List[HeaderRule]] = []
    media_types: Optional[List[MediaTypeRule]] = []
    conventions: Optional[List[HTTPConventionRule]] = []
