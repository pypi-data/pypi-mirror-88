from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, HttpUrl


class URLModel(BaseModel):
    value: HttpUrl


class URL(Scalar):
    """URL: Schema http or https, TLD required, max length 2083"""

    @staticmethod
    def serialize(value):
        return URLModel(value=value).value

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return URLModel(value=node.value).value

    @staticmethod
    def parse_value(value):
        return URLModel(value=value).value
