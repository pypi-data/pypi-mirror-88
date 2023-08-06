from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, PositiveFloat


class PositiveFloatModel(BaseModel):
    value: PositiveFloat


class PositiveFloat(Scalar):
    """PositiveFloat: Floats that will have a value greater than 0"""

    @staticmethod
    def serialize(value):
        return PositiveFloatModel(value=value).value

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return PositiveFloatModel(value=node.value).value

    @staticmethod
    def parse_value(value):
        return PositiveFloatModel(value=value).value
