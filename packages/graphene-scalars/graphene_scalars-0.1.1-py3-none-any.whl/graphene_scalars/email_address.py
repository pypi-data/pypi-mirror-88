from graphene.types import Scalar
from graphql.language import ast
from pydantic import BaseModel, EmailStr


class EmailAddressModel(BaseModel):
    value: EmailStr


class EmailAddress(Scalar):
    """EmailAddres: the input string must be a valid email address, and the output is a simple string"""

    @staticmethod
    def serialize(value):
        return EmailAddressModel(value=value).value

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return EmailAddressModel(value=node.value).value

    @staticmethod
    def parse_value(value):
        return EmailAddressModel(value=value).value
