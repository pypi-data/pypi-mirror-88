from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, PositiveInt


class PositiveIntModel(BaseModel):
    value: PositiveInt


class PositiveInt(Scalar):
    """PositiveInt: Integers that will have a value greater than 0"""

    @staticmethod
    def serialize(value):
        return PositiveIntModel(value=value).value

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return PositiveIntModel(value=node.value).value

    @staticmethod
    def parse_value(value):
        return PositiveIntModel(value=value).value
