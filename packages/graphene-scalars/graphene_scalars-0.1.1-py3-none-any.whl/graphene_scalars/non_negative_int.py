from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, validator


class NonNegativeIntModel(BaseModel):
    value: int

    @validator("value")
    def value_greater_equal_zero(v):
        assert int(v), "value must be int"
        assert v >= 0, "value must be greater than or equal to zero"
        return v


class NonNegativeInt(Scalar):
    """NonNegativeInt: Integers that will have a value of 0 or more"""

    @staticmethod
    def serialize(value):
        return NonNegativeIntModel(value=value).value

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return NonNegativeIntModel(value=node.value).value

    @staticmethod
    def parse_value(value):
        return NonNegativeIntModel(value=value).value
