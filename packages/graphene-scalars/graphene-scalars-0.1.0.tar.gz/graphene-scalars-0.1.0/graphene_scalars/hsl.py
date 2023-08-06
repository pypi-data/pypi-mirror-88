from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, validator
from pydantic.color import Color


class HSLModel(BaseModel):
    value: Color

    @validator("value")
    def value_as_hsl(cls, v):
        return Color(v).as_hsl()


class HSL(Scalar):
    """HSL: A field whose value is a CSS HSL color"""

    @staticmethod
    def serialize(value):
        return HSLModel(value=value).value

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return HSLModel(value=node.value).value

    @staticmethod
    def parse_value(value):
        return HSLModel(value=value).value
