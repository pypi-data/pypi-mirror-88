from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, validator


class NonEmptyStringModel(BaseModel):
    value: str

    @validator("value")
    def value_non_empty_string(v):
        assert str(v), "value must be string"
        assert v != "", "value cannot be empty"
        return v


class NonEmptyString(Scalar):
    """NonEmptyString: allows a str, use
    standard str parsing and then check
    the value is different from empty string."""

    @staticmethod
    def serialize(value):
        return NonEmptyStringModel(value=value).value

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return NonEmptyStringModel(value=node.value).value

    @staticmethod
    def parse_value(value):
        return NonEmptyStringModel(value=value).value
