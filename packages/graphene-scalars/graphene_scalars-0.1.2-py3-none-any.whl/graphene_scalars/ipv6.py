from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, validator
from ipaddress import IPv6Address


class IPv6Model(BaseModel):
    value: IPv6Address

    @validator("value")
    def value_validate(cls, v):
        return str(v)


class IPv6(Scalar):
    """IPv6: A field whose value is a IPv6 address"""

    @staticmethod
    def serialize(value):
        return IPv6Model(value=value).value

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return IPv6Model(value=node.value).value

    @staticmethod
    def parse_value(value):
        return IPv6Model(value=value).value
