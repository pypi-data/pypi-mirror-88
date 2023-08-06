from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, confloat


class NonPositiveFloatModel(BaseModel):
    value: confloat(le=0)


class NonPositiveFloat(Scalar):
    """NonPositiveFloat: Floats that will have a value of 0 or more"""

    @staticmethod
    def serialize(value):
        return NonPositiveFloatModel(value=value).value

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return NonPositiveFloatModel(value=node.value).value

    @staticmethod
    def parse_value(value):
        return NonPositiveFloatModel(value=value).value
