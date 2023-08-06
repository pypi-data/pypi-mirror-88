from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, UUID1


class UUIDModel(BaseModel):
    value: UUID1


class UUID(Scalar):
    """UUID: A field whose value is a generic Universally Unique Identifier"""

    @staticmethod
    def serialize(value):
        return str(UUIDModel(value=value).value)

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return UUIDModel(value=node.value).value

    @staticmethod
    def parse_value(value):
        return str(UUIDModel(value=value).value)
