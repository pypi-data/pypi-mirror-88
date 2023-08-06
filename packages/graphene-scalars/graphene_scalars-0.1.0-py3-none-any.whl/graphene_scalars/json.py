from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, Json


class JSONModel(BaseModel):
    value: Json


class JSON(Scalar):
    """JSON: The JSON scalar type represents JSON values as specified by ECMA-404"""

    @staticmethod
    def serialize(value):
        return JSONModel(value=value).value

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return JSONModel(value=node.value).value

    @staticmethod
    def parse_value(value):
        return JSONModel(value=value).value
