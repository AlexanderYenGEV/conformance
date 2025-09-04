from __future__ import annotations
from datetime import datetime, timedelta
from openapi_schema_validator import OAS30Validator
from enum import Enum, StrEnum, auto
from logging import info, warning
from typing import Optional, Protocol, runtime_checkable
import jsonschema
import requests
import os
import pytz
import yaml
from dataclasses import dataclass, field


class _CaseMatchingStrEnum(StrEnum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class Role(_CaseMatchingStrEnum):
    RATINGS_PROVIDER = auto()
    UNAUTHENTICATED = auto()


class Header(_CaseMatchingStrEnum):
    Authorization = auto()
    Accept = auto()
    Accept_Encoding = "Accept-Encoding"
    ContentType = "Content-Type"
    If_None_Match = "If-None-Match"
    Set_Server_Time = "X-TROLIE-Testing-Current-DateTime"


@runtime_checkable
class AuthTokenProvider(Protocol):
    def get_auth_token(self, role: Role) -> Optional[str]: ...


class TrolieClient:
    def __init__(self, role: Role):
        auth_token = TrolieClient.__get_auth_token(role)
        if auth_token is None and role != Role.UNAUTHENTICATED:
            raise ValueError(f"Failed to obtain Authentication token required for role {role}")
        self.auth_token = auth_token
        self.__headers = {}
        if role != Role.UNAUTHENTICATED:
            self.__headers["X-TROLIE-Testing-Identity"] = TrolieClient.__get_testing_identity(role)
        self.__body = None
        self.__method = None
        self.__trolie_url = None
        self.__query_params = {}
        self.role = role
        self.__response = None

    def request(self, relative_path, method="GET") -> TrolieClient:
        self.__trolie_url = TrolieClient.__get_trolie_url(relative_path)
        self.__method = method
        self.__relative_path = relative_path
        if self.auth_token:
            self.__headers["Authorization"] = f"Bearer {self.auth_token}"
        return self.send()

    def send(self) -> TrolieClient:
        self.__response = requests.request(
            method=self.__method,
            url=self.__trolie_url,
            headers=self.__headers,
            params=self.__query_params,
            json=self.__body,
            verify=False,  # Disable SSL verification for testing purposes
        )
        return self

    def set_body(self, body) -> TrolieClient:
        self.__body = body
        return self

    def set_header(self, key: Header, value: str) -> TrolieClient:
        self.__headers[key] = value
        return self

    def set_server_time(self, time: datetime) -> TrolieClient:
        self.set_header(Header.Set_Server_Time, time)
        return self

    def set_query_param(self, key: str, value: str | int) -> TrolieClient:
        self.__query_params[key] = value
        return self

    def ensure_empty_request(self) -> TrolieClient:
        if existing := self.__headers.pop(Header.ContentType, None):
            warning(f"Removing existing Content-Type header: {existing}")
        if self.__body:
            warning(f"Removing existing body: {self.__body}")
            self.__body = None
        return self

    def get_response_header(self, key: Header) -> int | str | None:
        if self.__response is not None:
            if key in self.__response.headers:
                value = self.__response.headers[key]
                return int(value) if value.isdigit() else value
        return None

    def get_json(self):
        return self.__response.json()

    def get_status_code(self) -> int:
        return self.__response.status_code

    def response_is_empty(self) -> bool:
        return len(self.__response.content) == 0

    def get_server_time(self): 
        return self.__headers["X-TROLIE-Testing-Current-DateTime"]

    @dataclass
    class ResponseInfo:
        verb: str
        relative_path: str
        content_type: str
        status_code: str
        body: dict

    def validate_response(self) -> bool:
        if content_type := self.get_response_header(Header.ContentType):
            if _ := MediaTypes(MediaType.from_string(content_type)):
                nfo = self.ResponseInfo(
                    verb=self.__response.request.method,
                    relative_path=self.__relative_path,
                    content_type=content_type,
                    status_code=str(self.get_status_code()),
                    body=self.get_json(),
                )
                return TrolieMessage.is_valid(nfo)
            else:
                warning(f"Unknown media type: {content_type}")
        else:
            warning("Missing Content-Type header")
        return False

    @staticmethod
    def __get_testing_identity(role: Role) -> Optional[str]:
        if role == Role.UNAUTHENTICATED:
            return None
        if role == Role.RATINGS_PROVIDER:
            return "TO1"

    def __get_auth_token(role: Role) -> Optional[str]:
        if role == Role.UNAUTHENTICATED:
            return None

        if auth_token_provider := TrolieClient.__load_auth_token_provider():
            if token := auth_token_provider.get_auth_token(role):
                return token
            else:
                warning(f"Token Provider Failed to obtain token for role {role}")
        else:
            info("No AuthTokenProvider found")

        if token := os.getenv(f"{role}_TOKEN"):
            return token

        raise ValueError(f"Missing {role}_TOKEN environment variable")

    @staticmethod
    def __load_auth_token_provider() -> Optional[AuthTokenProvider]:
        if hasattr(TrolieClient, "_auth_token_provider"):
            return TrolieClient._auth_token_provider

        try:
            from test import auth_token_provider
        except ImportError as e: 
            warning(f"ImportError when importing auth_token_provider: {e}")

        for attr_name in dir(auth_token_provider):
            if attr_name == "AuthTokenProvider":
                # avoid instantiating the protocol if it's imported for some reason
                continue
            attr = getattr(auth_token_provider, attr_name)
            if isinstance(attr, type) and issubclass(attr, AuthTokenProvider):
                TrolieClient._auth_token_provider = attr()
                return TrolieClient._auth_token_provider

        return None

    @staticmethod
    def __get_trolie_url(relative_path):
        return os.getenv("TROLIE_BASE_URL") + relative_path


@dataclass
class MediaType:
    contentType: str
    parameters: dict = field(default_factory=dict)

    def __str__(self):
        params = "; ".join(f"{k}={v}" for k, v in self.parameters.items())
        return f"{self.contentType}; {params}"

    def __eq__(self, other):
        if not isinstance(other, MediaType):
            return NotImplemented
        return self.contentType == other.contentType and self.parameters == other.parameters

    @staticmethod
    def from_string(media_type_str: str) -> "MediaType":
        parts = media_type_str.split(";")
        contentType = parts[0].strip()
        parameters = {}
        if len(parts) > 1:
            param_str = parts[1].strip()
            for param in param_str.split(","):
                key, value = param.strip().split("=")
                parameters[key] = value
        return MediaType(contentType=contentType, parameters=parameters)


# Function to load media types from openapi.yaml
def load_media_types_from_yaml(file_path: str) -> dict:
    with open(file_path, "r") as file:
        openapi_spec = yaml.safe_load(file)

    media_types = {}
    for _, path_item in openapi_spec.get("paths", {}).items():
        for operation in path_item.values():
            if "requestBody" in operation:
                content = operation["requestBody"].get("content", {})
                for media_type in content.keys():
                    media_types[media_type] = MediaType.from_string(media_type)
            for response in operation.get("responses", {}).values():
                content = response.get("content", {})
                for media_type in content.keys():
                    media_types[media_type] = MediaType.from_string(media_type)
    return media_types


media_types = load_media_types_from_yaml("openapi.yaml")

MediaTypes = Enum("MediaTypes", media_types)


class TrolieMessage:
    @staticmethod
    def is_valid(response: TrolieClient.ResponseInfo) -> bool:
        with open("openapi.yaml") as f:
            openapi_spec = yaml.safe_load(f)
        schema = TrolieMessage.get_response_schema(response, openapi_spec)
        rooted_schemas = {"components": {"schemas": openapi_spec["components"]["schemas"]}}
        ref_resolver = jsonschema.RefResolver.from_schema(rooted_schemas)
        validator = OAS30Validator(schema, resolver=ref_resolver)
        try:
            validator.validate(instance=response.body)
        except jsonschema.ValidationError as e:
            warning(f"Message failed validation: {e}")
            return False
        return True

    @staticmethod
    def _safe_get(d, keys):
        _d = d.copy()
        for key in keys:
            try:
                if "$ref" in _d:
                    ref = _d["$ref"]
                    ref_parts = ref.removeprefix("#/").split("/")
                    _d = d[ref_parts[0]][ref_parts[1]][ref_parts[2]]
                _d = _d[key]
            except (KeyError, TypeError):
                raise ValueError(f"Key not found: {key} in child {_d} of {d}")
        return _d

    @staticmethod
    def get_response_schema(response: TrolieClient.ResponseInfo, openapi_spec: dict) -> dict:
        content_info_path = [
            "paths",
            response.relative_path,
            response.verb.lower(),
            "responses",
            response.status_code,
            "content",
            response.content_type,
        ]
        content_info = TrolieMessage._safe_get(openapi_spec, content_info_path)
        if "$ref" in content_info["schema"]:
            schema_ref = content_info["schema"]["$ref"]
            schema_name = schema_ref.split("/")[-1]
            return openapi_spec["components"]["schemas"][schema_name]
        return content_info["schema"]


def get_period(hours=0):
    tz_name = os.getenv("TZ", "UTC")
    timezone = pytz.timezone(tz_name)
    return (datetime.now(timezone) + timedelta(hours=hours)).replace(minute=0, second=0, microsecond=0).isoformat()
