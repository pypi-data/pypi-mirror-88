from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, validator


class NonPositiveIntModel(BaseModel):
    value: int

    @validator("value")
    def value_greater_equal_zero(v):
        assert int(v), "value must be int"
        assert v <= 0, "value must be less than or equal to zero"
        return v


class NonPositiveInt(Scalar):
    """NonPositiveInt: Integers that will have a value of 0 or less"""

    @staticmethod
    def serialize(value):
        return NonPositiveIntModel(value=value).value

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return NonPositiveIntModel(value=node.value).value

    @staticmethod
    def parse_value(value):
        return NonPositiveIntModel(value=value).value
