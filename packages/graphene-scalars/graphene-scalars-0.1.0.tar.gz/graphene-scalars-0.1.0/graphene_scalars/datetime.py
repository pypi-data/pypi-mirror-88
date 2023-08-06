from datetime import datetime as dt
from graphene.types import Scalar
from graphql.language import ast


format = "%Y-%m-%dT%H:%M:%S.%f"


class Datetime(Scalar):
    """Datetime: in ISO 8601 format,
    similar to the format returned by
    'new Date (). ToISOString ()' in javascript."""

    @staticmethod
    def serialize(value):
        return f"{dt.strptime(value[:-1], format).isoformat()[:-3]}Z"

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return f"{dt.strptime(node.value[:-1], format).isoformat()[:-3]}Z"

    @staticmethod
    def parse_value(value):
        return f"{dt.strptime(value[:-1], format).isoformat()[:-3]}Z"
