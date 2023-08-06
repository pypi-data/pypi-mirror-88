from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, conint


class NonPositiveIntModel(BaseModel):
    value: conint(le=0)


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
