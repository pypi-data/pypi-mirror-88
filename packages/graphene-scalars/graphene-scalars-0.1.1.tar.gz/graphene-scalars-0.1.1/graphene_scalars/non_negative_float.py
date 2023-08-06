from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, validator


class NonNegativeFloatModel(BaseModel):
    value: float

    @validator("value")
    def value_greater_equal_zero(v):
        assert float(v), "value must be float"
        assert v >= 0, "value must be greater than or equal to zero"
        return v


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
