from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, validator
from pydantic.color import Color


class ColorHexModel(BaseModel):
    value: Color

    @validator("value")
    def value_as_hex(v):
        return Color(v).as_hex()


class ColorHex(Scalar):
    """ColorHex: A field whose value is a hexadecimal"""

    @staticmethod
    def serialize(value):
        return ColorHexModel(value=value).value

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return ColorHexModel(value=node.value).value

    @staticmethod
    def parse_value(value):
        return ColorHexModel(value=value).value
