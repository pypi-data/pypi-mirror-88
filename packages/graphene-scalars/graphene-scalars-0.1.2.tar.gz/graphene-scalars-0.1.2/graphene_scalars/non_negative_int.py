from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, conint


class NonNegativeIntModel(BaseModel):
    value: conint(ge=0)


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
