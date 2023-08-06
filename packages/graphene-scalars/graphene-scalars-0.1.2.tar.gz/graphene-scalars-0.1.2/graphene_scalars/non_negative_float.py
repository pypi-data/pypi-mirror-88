from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, confloat


class NonNegativeFloatModel(BaseModel):
    value: confloat(ge=0)


class NonNegativeFloat(Scalar):
    """NonNegativeFloat: Floats that will have a value of 0 or more"""

    @staticmethod
    def serialize(value):
        return NonNegativeFloatModel(value=value).value

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return NonNegativeFloatModel(value=node.value).value

    @staticmethod
    def parse_value(value):
        return NonNegativeFloatModel(value=value).value
