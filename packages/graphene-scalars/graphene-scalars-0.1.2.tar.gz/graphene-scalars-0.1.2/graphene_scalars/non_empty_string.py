from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, constr, root_validator


class NonEmptyStringModel(BaseModel):
    value: constr(regex="^[\w\W]+([\s][\w\W]+)*$")

    @root_validator(pre=True)
    def format_value(cls, values):
        values.update(value=values.get("value").strip())
        return values


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
