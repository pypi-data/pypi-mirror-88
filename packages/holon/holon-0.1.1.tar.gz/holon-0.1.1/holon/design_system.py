from enum import Enum

# from holon.conventions import Convention
from holon.protocols.http import HTTPMessage, HTTPMethod, HTTPRuleSet
from holon.principles import Principle, PrincipleRule
from holon.base import autocomplete, BaseModel
from holon.ietf.rfc2119 import Keyword
from typing import List, Optional


# @autocomplete
# class PrincipleRule(BaseModel):
#     keyword: Keyword
#     principle: Principle


# @autocomplete
# class HeaderRule(BaseModel):
#     keyword: Keyword
#     header: Header


# @autocomplete
# class MediaTypeRule(BaseModel):
#     keyword: Keyword
#     media_type: MediaType


# @autocomplete
# class ConventionRule(BaseModel):
#     keyword: Keyword
#     convention: Convention


# @autocomplete
# class HTTPConventionRule(BaseModel):
#     keyword: Keyword
#     convention: Convention
#     element: Optional[http.HTTPElement] = None
#     method: Optiona[http.HTTPMethod] = None
#     message: Optional[http.HTTPMessage] = None


# @autocomplete
# class HTTPRuleSet(BaseModel):
#     headers: Optional[List[HeaderRule]] = []
#     media_types: Optional[List[MediaTypeRule]] = []
#     http_conventions: Optional[List[HTTPConventionRule]] = []


@autocomplete
class APIDesignSystem(BaseModel):
    principles: Optional[List[PrincipleRule]] = []
    http_rules: Optional[HTTPRuleSet] = None
