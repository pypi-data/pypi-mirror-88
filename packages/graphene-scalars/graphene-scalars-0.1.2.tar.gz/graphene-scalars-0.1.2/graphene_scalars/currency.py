from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, condecimal


class CurrencyModel(BaseModel):
    value: condecimal(decimal_places=2, gt=0)


class Currency(Scalar):
    """Currency: A US currency string, such as 21.25"""

    @staticmethod
    def serialize(value):
        return float(CurrencyModel(value=value).value)

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return float(CurrencyModel(value=node.value).value)

    @staticmethod
    def parse_value(value):
        return float(CurrencyModel(value=value).value)
