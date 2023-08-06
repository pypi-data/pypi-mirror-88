from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, validator
from pydantic.color import Color


class RGBModel(BaseModel):
    value: Color

    @validator("value")
    def value_as_rgb(cls, v):
        return Color(v).as_rgb()


class RGB(Scalar):
    """RGB: A field whose value is a CSS RGB color"""

    @staticmethod
    def serialize(value):
        return RGBModel(value=value).value

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return RGBModel(value=node.value).value

    @staticmethod
    def parse_value(value):
        return RGBModel(value=value).value
