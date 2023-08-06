from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, validator
from ipaddress import IPv4Address


class IPv4Model(BaseModel):
    value: IPv4Address

    @validator("value")
    def value_validate(v):
        return str(v)


class IPv4(Scalar):
    """IPv4: A field whose value is a IPv4 address"""

    @staticmethod
    def serialize(value):
        return IPv4Model(value=value).value

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return IPv4Model(value=node.value).value

    @staticmethod
    def parse_value(value):
        return IPv4Model(value=value).value
