"""
A majority of this file is copied from FastAPI.
https://github.com/tiangolo/fastapi
"""

from enum import Enum
from typing import Any, Callable, Dict, Iterable, List, Literal, Optional, Union

from holon.base import autocomplete
from pydantic import AnyUrl, BaseModel, Field


@autocomplete
class Contact(BaseModel):
    name: Optional[str] = None
    url: Optional[AnyUrl] = None
    email: Optional[str] = None


@autocomplete
class License(BaseModel):
    name: str
    url: Optional[AnyUrl] = None


@autocomplete
class Info(BaseModel):
    title: str
    version: str
    description: Optional[str] = None
    termsOfService: Optional[str] = None
    contact: Optional[Contact] = None
    license: Optional[License] = None


@autocomplete
class ServerVariable(BaseModel):
    default: str
    enum: Optional[List[str]] = None
    description: Optional[str] = None


@autocomplete
class Server(BaseModel):
    url: Union[AnyUrl, str]
    description: Optional[str] = None
    variables: Optional[Dict[str, ServerVariable]] = None


class Reference(BaseModel):
    ref: str = Field(..., alias="$ref")


@autocomplete
class Discriminator(BaseModel):
    propertyName: str
    mapping: Optional[Dict[str, str]] = None


@autocomplete
class XML(BaseModel):
    name: Optional[str] = None
    namespace: Optional[str] = None
    prefix: Optional[str] = None
    attribute: Optional[bool] = None
    wrapped: Optional[bool] = None


@autocomplete
class ExternalDocumentation(BaseModel):
    url: AnyUrl
    description: Optional[str] = None


@autocomplete
class SchemaBase(BaseModel):
    ref: Optional[str] = Field(None, alias="$ref")
    title: Optional[str] = None
    multipleOf: Optional[float] = None
    maximum: Optional[float] = None
    exclusiveMaximum: Optional[float] = None
    minimum: Optional[float] = None
    exclusiveMinimum: Optional[float] = None
    maxLength: Optional[int] = Field(None, gte=0)
    minLength: Optional[int] = Field(None, gte=0)
    pattern: Optional[str] = None
    maxItems: Optional[int] = Field(None, gte=0)
    minItems: Optional[int] = Field(None, gte=0)
    uniqueItems: Optional[bool] = None
    maxProperties: Optional[int] = Field(None, gte=0)
    minProperties: Optional[int] = Field(None, gte=0)
    required: Optional[List[str]] = None
    enum: Optional[List[Any]] = None
    type: Optional[str] = None
    allOf: Optional[List[Any]] = None
    oneOf: Optional[List[Any]] = None
    anyOf: Optional[List[Any]] = None
    not_: Optional[Any] = Field(None, alias="not")
    items: Optional[Any] = None
    properties: Optional[Dict[str, Any]] = None
    additionalProperties: Optional[Union[Dict[str, Any], bool]] = None
    description: Optional[str] = None
    format: Optional[str] = None
    default: Optional[Any] = None
    nullable: Optional[bool] = None
    discriminator: Optional[Discriminator] = None
    readOnly: Optional[bool] = None
    writeOnly: Optional[bool] = None
    xml: Optional[XML] = None
    externalDocs: Optional[ExternalDocumentation] = None
    example: Optional[Any] = None
    deprecated: Optional[bool] = None


@autocomplete
class Schema(SchemaBase):
    allOf: Optional[List[SchemaBase]] = None
    oneOf: Optional[List[SchemaBase]] = None
    anyOf: Optional[List[SchemaBase]] = None
    not_: Optional[SchemaBase] = Field(None, alias="not")
    items: Optional[SchemaBase] = None
    properties: Optional[Dict[str, SchemaBase]] = None
    additionalProperties: Optional[Union[Dict[str, Any], bool]] = None


@autocomplete
class Example(BaseModel):
    summary: Optional[str] = None
    description: Optional[str] = None
    value: Optional[Any] = None
    externalValue: Optional[AnyUrl] = None


@autocomplete
class ParameterInType(Enum):
    query = "query"
    header = "header"
    path = "path"
    cookie = "cookie"


@autocomplete
class Encoding(BaseModel):
    contentType: Optional[str] = None
    # Workaround OpenAPI recursive reference, using Any
    headers: Optional[Dict[str, Union[Any, Reference]]] = None
    style: Optional[str] = None
    explode: Optional[bool] = None
    allowReserved: Optional[bool] = None


@autocomplete
class MediaType(BaseModel):
    schema_: Optional[Union[Schema, Reference]] = Field(None, alias="schema")
    example: Optional[Any] = None
    examples: Optional[Dict[str, Union[Example, Reference]]] = None
    encoding: Optional[Dict[str, Encoding]] = None


@autocomplete
class ParameterBase(BaseModel):
    description: Optional[str] = None
    required: Optional[bool] = None
    deprecated: Optional[bool] = None
    # Serialization rules for simple scenarios
    style: Optional[str] = None
    explode: Optional[bool] = None
    allowReserved: Optional[bool] = None
    schema_: Optional[Union[Schema, Reference]] = Field(None, alias="schema")
    example: Optional[Any] = None
    examples: Optional[Dict[str, Union[Example, Reference]]] = None
    # Serialization rules for more complex scenarios
    content: Optional[Dict[str, MediaType]] = None


@autocomplete
class Parameter(ParameterBase):
    name: str  # type: ignore
    in_: ParameterInType = Field(..., alias="in")


@autocomplete
class Header(ParameterBase):
    pass


# Workaround OpenAPI recursive reference
@autocomplete
class EncodingWithHeaders(Encoding):
    headers: Optional[Dict[str, Union[Header, Reference]]] = None


@autocomplete
class RequestBody(BaseModel):
    description: Optional[str] = None
    content: Dict[str, MediaType]  # type: ignore
    required: Optional[bool] = None


@autocomplete
class Link(BaseModel):
    operationRef: Optional[str] = None
    operationId: Optional[str] = None
    parameters: Optional[Dict[str, Union[Any, str]]] = None
    requestBody: Optional[Union[Any, str]] = None
    description: Optional[str] = None
    server: Optional[Server] = None


@autocomplete
class Response(BaseModel):
    description: str
    headers: Optional[Dict[str, Union[Header, Reference]]] = None
    content: Optional[Dict[str, MediaType]] = None
    links: Optional[Dict[str, Union[Link, Reference]]] = None


@autocomplete
class Operation(BaseModel):
    tags: Optional[List[str]] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    externalDocs: Optional[ExternalDocumentation] = None
    operationId: Optional[str] = None
    parameters: Optional[List[Union[Parameter, Reference]]] = None
    requestBody: Optional[Union[RequestBody, Reference]] = None
    responses: Dict[str, Response]  # type: ignore
    # Workaround OpenAPI recursive reference
    callbacks: Optional[Dict[str, Union[Dict[str, Any], Reference]]] = None
    deprecated: Optional[bool] = None
    security: Optional[List[Dict[str, List[str]]]] = None
    servers: Optional[List[Server]] = None


@autocomplete
class PathItem(BaseModel):
    ref: Optional[str] = Field(None, alias="$ref")
    summary: Optional[str] = None
    description: Optional[str] = None
    get: Optional[Operation] = None
    put: Optional[Operation] = None
    post: Optional[Operation] = None
    delete: Optional[Operation] = None
    options: Optional[Operation] = None
    head: Optional[Operation] = None
    patch: Optional[Operation] = None
    trace: Optional[Operation] = None
    servers: Optional[List[Server]] = None
    parameters: Optional[List[Union[Parameter, Reference]]] = None


# Workaround OpenAPI recursive reference
@autocomplete
class OperationWithCallbacks(BaseModel):
    callbacks: Optional[Dict[str, Union[Dict[str, PathItem], Reference]]] = None


@autocomplete
class SecuritySchemeType(Enum):
    apiKey = "apiKey"
    http = "http"
    oauth2 = "oauth2"
    openIdConnect = "openIdConnect"


@autocomplete
class SecurityBase(BaseModel):
    type_: SecuritySchemeType = Field(..., alias="type")
    description: Optional[str] = None


@autocomplete
class APIKeyIn(Enum):
    query = "query"
    header = "header"
    cookie = "cookie"


@autocomplete
class APIKey(SecurityBase):
    type_ = Field(SecuritySchemeType.apiKey, alias="type")
    in_: APIKeyIn = Field(..., alias="in")
    name: str  # type: ignore


@autocomplete
class HTTPBase(SecurityBase):
    type_ = Field(SecuritySchemeType.http, alias="type")
    scheme: str  # type: ignore


@autocomplete
class HTTPBearer(HTTPBase):  # type: ignore
    scheme = "bearer"
    bearerFormat: Optional[str] = None


@autocomplete
class OAuthFlow(BaseModel):
    refreshUrl: Optional[str] = None
    scopes: Dict[str, str] = {}


@autocomplete
class OAuthFlowImplicit(OAuthFlow):
    authorizationUrl: str  # type: ignore


@autocomplete
class OAuthFlowPassword(OAuthFlow):
    tokenUrl: str  # type: ignore


@autocomplete
class OAuthFlowClientCredentials(OAuthFlow):
    tokenUrl: str  # type: ignore


@autocomplete
class OAuthFlowAuthorizationCode(OAuthFlow):
    authorizationUrl: str  # type: ignore
    tokenUrl: str  # type: ignore


@autocomplete
class OAuthFlows(BaseModel):
    implicit: Optional[OAuthFlowImplicit] = None
    password: Optional[OAuthFlowPassword] = None
    clientCredentials: Optional[OAuthFlowClientCredentials] = None
    authorizationCode: Optional[OAuthFlowAuthorizationCode] = None


@autocomplete
class OAuth2(SecurityBase):
    type_ = Field(SecuritySchemeType.oauth2, alias="type")
    flows: OAuthFlows  # type: ignore


@autocomplete
class OpenIdConnect(SecurityBase):
    type_ = Field(SecuritySchemeType.openIdConnect, alias="type")
    openIdConnectUrl: str  # type: ignore


SecurityScheme = Union[APIKey, HTTPBase, OAuth2, OpenIdConnect, HTTPBearer]


@autocomplete
class Components(BaseModel):
    schemas: Optional[Dict[str, Union[Schema, Reference]]] = None
    responses: Optional[Dict[str, Union[Response, Reference]]] = None
    parameters: Optional[Dict[str, Union[Parameter, Reference]]] = None
    examples: Optional[Dict[str, Union[Example, Reference]]] = None
    requestBodies: Optional[Dict[str, Union[RequestBody, Reference]]] = None
    headers: Optional[Dict[str, Union[Header, Reference]]] = None
    securitySchemes: Optional[Dict[str, Union[SecurityScheme, Reference]]] = None
    links: Optional[Dict[str, Union[Link, Reference]]] = None
    callbacks: Optional[Dict[str, Union[Dict[str, PathItem], Reference]]] = None


@autocomplete
class Tag(BaseModel):
    name: str
    description: Optional[str] = None
    externalDocs: Optional[ExternalDocumentation] = None


@autocomplete
class OpenAPI(BaseModel):
    openapi: Literal["3.0.0"] = "3.0.0"
    info: Info  # type: ignore
    servers: Optional[List[Server]] = None
    paths: Dict[str, PathItem]  # type: ignore
    components: Optional[Components] = None
    security: Optional[List[Dict[str, List[str]]]] = None
    tags: Optional[List[Tag]] = None
    externalDocs: Optional[ExternalDocumentation] = None
