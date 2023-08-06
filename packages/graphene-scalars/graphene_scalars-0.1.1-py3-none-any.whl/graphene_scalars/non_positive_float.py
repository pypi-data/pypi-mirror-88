from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, validator


class NonPositiveFloatModel(BaseModel):
    value: float

    @validator("value")
    def value_greater_equal_zero(v):
        assert float(v), "value must be float"
        assert v <= 0, "value must be less than or equal to zero"
        return v


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
