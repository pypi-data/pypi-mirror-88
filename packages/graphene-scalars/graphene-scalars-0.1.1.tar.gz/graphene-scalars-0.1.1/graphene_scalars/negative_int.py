from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, NegativeInt


class NegativeIntModel(BaseModel):
    value: NegativeInt


class NegativeInt(Scalar):
    """NegativeInt: Integers that will have a value less than 0"""

    @staticmethod
    def serialize(value):
        return NegativeIntModel(value=value).value

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return NegativeIntModel(value=node.value).value

    @staticmethod
    def parse_value(value):
        return NegativeIntModel(value=value).value
