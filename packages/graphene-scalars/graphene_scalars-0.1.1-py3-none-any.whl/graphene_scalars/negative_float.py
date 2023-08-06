from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, NegativeFloat


class NegativeFloatModel(BaseModel):
    value: NegativeFloat


class NegativeFloat(Scalar):
    """NegativeFloat: Floats that will have a value less than 0"""

    @staticmethod
    def serialize(value):
        return NegativeFloatModel(value=value).value

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return NegativeFloatModel(value=node.value).value

    @staticmethod
    def parse_value(value):
        return NegativeFloatModel(value=value).value
