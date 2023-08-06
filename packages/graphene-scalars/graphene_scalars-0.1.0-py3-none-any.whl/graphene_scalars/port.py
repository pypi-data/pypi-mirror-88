from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, conint


class PortModel(BaseModel):
    value: conint(ge=0, le=65535)


class Port(Scalar):
    """Port: A field whose value is a valid TCP port within the range of 0 to 65535"""

    @staticmethod
    def serialize(value):
        return PortModel(value=value).value

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return PortModel(value=node.value).value

    @staticmethod
    def parse_value(value):
        return PortModel(value=value).value
